import logging
from decimal import Decimal
import os
from datetime import date
from dataclasses import dataclass
import base64
import typing
import uuid
from PIL import Image
from io import BytesIO
import requests
from asgiref.sync import async_to_sync
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from django.db.models.manager import BaseManager
from django.core.files.base import ContentFile
from api import models, serializers, utils
from api.senders import send_admin_notification, NotifyLevels, send_order_created, send_chat_message


PAYMENTS_URL = f'{os.environ.get("PAYMENTS_SCHEMA")}://{os.environ.get("PAYMENTS_HOST")}'
if os.environ.get("PAYMENTS_PORT"):
    PAYMENTS_URL += f':{os.environ.get("PAYMENTS_PORT")}'


class Orders(APIView):
    @utils.auth_required
    def get(self, request: Request, profile: models.Profile):
        offset = request.data.get('offset', 0)
        limit = request.data.get('limit', 20)
        response = serializers.OrderSerializer(
            models.Order.objects.filter(profile=profile).distinct().order_by('-date')[offset:limit],
            many=True,
        ).data
        return Response(response)


class CheckPromoCode(APIView):
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        promo_code = request.data.get('promoCode')
        if promo_code:
            promo = utils.check_promo_code(profile, promo_code)
            if promo:
                return Response({
                    'result': True,
                    'discount': promo,
                })
            return Response({'result': False})
        return Response(status=status.HTTP_400_BAD_REQUEST)


@dataclass
class OrderInfo:
    profile: models.Profile
    cart: list[models.AbstractProductPublication]
    spend_cashback: bool
    need_account: bool
    bill_email: str
    remember_account: bool
    email: str
    password: str
    promo_code: str
    spend_cashback_amount: int = 0
    
    def get_promo_code_discount(self) -> int | None:
        discount = utils.check_promo_code(self.profile, self.promo_code)
        if not discount:
            self.promo_code = None
            discount = 0
        return discount
    
    def get_amount(self, promo_code_discount: int = None) -> int:
        amount = sum([item.final_price for item in self.cart])
        if promo_code_discount:
            amount -= amount * promo_code_discount / 100
        if self.spend_cashback:
            if self.profile.cashback >= amount:
                self.spend_cashback_amount = amount - 10
                return 10
            self.spend_cashback_amount = self.profile.cashback
            amount -= self.spend_cashback_amount
        return amount
    
    def get_description(self, publication: models.AbstractProductPublication) -> str:
        description = f'{publication.title}'
        for platform in publication.platforms.all():
            description += f' - {platform.name}'
        return description
    
    def update_profile(self):
        if self.remember_account:
            self.profile.playstation_email = self.email
            self.profile.playstation_password = self.password
            self.profile.bill_email = self.bill_email
        if self.spend_cashback:
            self.profile.cashback -= self.spend_cashback_amount
        self.profile.save()
    
    def fill_order(self, order: models.Order, promo_code_discount: int) -> models.Order:
        self.update_profile()
        order.cashback = 0
        cart_sum = 0
        for publication in self.cart:
            final_price = publication.final_price - publication.final_price * promo_code_discount / 100
            if self.spend_cashback:
                if cart_sum + final_price > order.amount:
                    final_price = order.amount - cart_sum
                cart_sum += final_price
            if not self.spend_cashback:
                order.cashback += publication.final_price * publication.cashback / 100
            models.OrderProduct.objects.get_or_create(
                order=order,
                product=publication.product.title,
                product_id=publication.id,
                description=self.get_description(publication),
                final_price=Decimal(final_price),
            )
        if order.promo_code_discount:
            order.cashback -= order.cashback * promo_code_discount / 100
        payment = serializers.PaymentSerializer(
            data=requests.post(f'{PAYMENTS_URL}/create_payment',
                json=serializers.CreatePaymentSerializer(order).data,
            ).json()
        )
        if payment.is_valid():
            order.payment_id = payment.validated_data.get('payment_id')
            order.payment_url = payment.validated_data.get('payment_url')
            order.status = models.Order.StatusChoices.PAYMENT
        else:
            order.status = models.Order.StatusChoices.ERROR
        order.save()
        return order
    
    def create_order(self) -> models.Order:
        if not self.need_account:
            if not self.email:
                self.email = self.profile.playstation_email
            if not self.password:
                self.password = self.profile.playstation_password
        promo_code_discount = self.get_promo_code_discount()
        order, created = models.Order.objects.get_or_create(
            profile=self.profile,
            date=date.today(),
            amount=self.get_amount(promo_code_discount),
            need_account=self.need_account,
            email=self.email,
            password=self.password,
            bill_email=self.bill_email,
            spend_cashback=self.spend_cashback,
            status=models.Order.StatusChoices.PAYMENT,
            promo_code=self.promo_code,
            promo_code_discount=promo_code_discount,
            spend_cashback_amount=self.spend_cashback_amount,
        )
        if created:
            order = self.fill_order(order, promo_code_discount)
        return order


class CreateOrder(APIView):
    def get_cart(self, profile: models.Profile):
        cart = models.Cart.objects.get_or_create(profile=profile)[0]
        cart_items = list(cart.publications.all()) \
            + list(cart.add_ons.all()) \
            + list(cart.subscriptions.all())
        cart.delete()
        return cart_items
    
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        order_info = OrderInfo(
            profile,
            self.get_cart(profile),
            request.data.get('spendCashback', False),
            not request.data.get('hasAccount', False),
            request.data.get('billEmail', profile.bill_email),
            request.data.get('rememberAccount', False),
            request.data.get('accountEmail'),
            request.data.get('accountPassword'),
            request.data.get('promoCode'),
        )
        if not order_info.need_account:
            if not order_info.email:
                order_info.email = profile.playstation_email
            if not order_info.password:
                order_info.password = profile.playstation_password
        if order_info.cart and order_info.bill_email:
            order = order_info.create_order()
            async_to_sync(send_admin_notification)({'text': f'Новый заказ {order.id}',
                                                    'level': NotifyLevels.SUCCESS.value})
            return Response(
                {
                    'PaymentUrl': order.payment_url
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatMessages(APIView):
    def get(self, request: Request):
        return Response(
            serializers.ChatMessageSerializer(
                models.ChatMessage.objects.filter(order=request.query_params.get('order_id')),
                many=True,
            ).data,
            status=status.HTTP_200_OK
        )
        
    def post(self, request: Request):
        order_id = request.data.get('order_id')
        text = request.data.get('text')
        order = models.Order.objects.filter(id=order_id).first()
        if order and text:
            message = models.ChatMessage.objects.create(
                order=order,
                text=text,
            )
            for image in request.data.get('images', []):
                order_message_image = models.OrderMessageImage.objects.create(chat_message=message)
                img = Image.open(BytesIO(base64.b64decode(image)))
                img_io = BytesIO()
                img.save(img_io, format="WEBP", quality=50)
                img_io.seek(0)
                order_message_image.image.save(f'photo_{uuid.uuid4().hex}.webp', ContentFile(img_io.getvalue()), save=True)
            send_chat_message(message)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatus(APIView):
    def get_product_publication(self, id) -> models.AbstractProductPublication | None:
        result = models.Publication.objects.filter(id=id).first()
        if result is None:
            result = models.AddOn.objects.filter(id=id).first()
        if result is None:
            result = models.Subscription.objects.filter(id=id).first()
        return result
    
    def restore_cart(self, order: models.Order) -> models.Cart:
        cart = models.Cart.objects.get_or_create(profile=order.profile)[0]
        for item in models.OrderProduct.objects.filter(order=order):
            product_publication = self.get_product_publication(item.product_id)
            if product_publication:
                match product_publication.typename:
                    case 'publication':
                        cart.publications.add(product_publication)
                    case 'add_on':
                        cart.add_ons.add(product_publication)
                    case 'subscription':
                        cart.subscriptions.add(product_publication)
        return cart
    
    def post(self, request: Request):
        check_token = requests.post(PAYMENTS_URL+'/check_token', json=request.data).json()
        if check_token.get('TokenCorrect'):
            order = models.Order.objects.filter(id=request.data.get('OrderId')).first()
            if order:
                match request.data.get('Status'):
                    case 'CONFIRMED':
                        if order.status == models.Order.StatusChoices.PAID:
                            return Response('OK')
                        order.status = models.Order.StatusChoices.PAID
                        order.profile.cashback += order.cashback
                        order.profile.save()
                        order.save()
                        utils.update_sales_leaders(order)
                        async_to_sync(send_admin_notification)({
                            'text': f'Заказ {order.id} оплачен',
                            'level': NotifyLevels.SUCCESS.value
                        })
                        send_order_created(order)
                    case 'DEADLINE_EXPIRED':
                        order.profile.cashback += order.spend_cashback_amount
                        order.profile.save()
                        self.restore_cart(order)
                        order.delete()
                    case 'REJECTED'| 'REVERSED' | 'PARTIAL_REVERSED'| 'PARTIAL_REFUNDED'| 'REFUNDED':
                        async_to_sync(send_admin_notification)({'text': f'Заказ {order.id} не был оплачен за выделенное время',
                                                                'level': NotifyLevels.ERROR.value})
                        order.profile.cashback += order.spend_cashback_amount
                        order.profile.save()
                        order.status = models.Order.StatusChoices.ERROR
                        order.save()
        return Response('OK')
