import logging
from decimal import Decimal
from datetime import date, timedelta
from dataclasses import dataclass
import base64
import uuid
from PIL import Image
from io import BytesIO
import requests
from asgiref.sync import async_to_sync
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.files.base import ContentFile
from django.utils import timezone
from api import models, serializers, utils, tasks
from api.senders import send_admin_notification, NotifyLevels, send_order_created, send_chat_message
from settings import PAYMENTS_URL, DEBUG


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
            tasks.check_order_expired.apply_async(
                args=[str(order.id)],
                eta=timezone.now()+timedelta(minutes=30),
                task_id=f'check_order_{order.id}_expired'
            )
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
            if models.ChatMessage.objects.filter(order=order, manager=None).count() == 1:
                send_order_created(order)
            else:
                send_chat_message(message)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatus(APIView):
    def check_token(self, data: dict) -> bool:
        if DEBUG:
            return True
        check_token = requests.post(PAYMENTS_URL+'/check_token', json=data).json()
        return check_token.get('TokenCorrect')
    
    def order_paid(self, order: models.Order):
        if order.status != models.Order.StatusChoices.PAID:
            order.status = models.Order.StatusChoices.PAID
            order.profile.cashback += order.cashback
            order.profile.save()
            order.save()
            utils.update_sales_leaders(order)
            async_to_sync(send_admin_notification)({
                'text': f'Заказ {order.id} оплачен',
                'level': NotifyLevels.SUCCESS.value
            })
        return Response('OK')
    
    def order_rejected(self, order: models.Order):
        async_to_sync(send_admin_notification)({
            'text': f'Заказ {order.id} не был оплачен за выделенное время',
            'level': NotifyLevels.ERROR.value
        })
        order.profile.cashback += order.spend_cashback_amount
        order.profile.save()
        order.status = models.Order.StatusChoices.ERROR
        order.save()
        return Response('OK')
    
    def post(self, request: Request):
        if not self.check_token(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = models.Order.objects.filter(id=request.data.get('OrderId')).first()
        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        match request.data.get('Status'):
            case 'AUTHORIZED':
                return Response('OK')
            case 'CONFIRMED':
                return self.order_paid(order)
        return self.order_rejected(order)
