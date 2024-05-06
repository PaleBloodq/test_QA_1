import os
from datetime import date
from dataclasses import dataclass
import requests
from asgiref.sync import async_to_sync
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from django.db.models.manager import BaseManager
from api import models, serializers, utils
from api.senders import send_admin_notification, NotifyLevels

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
            promo = utils.check_promo_code(promo_code)
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
    cart: BaseManager[models.ProductPublication]
    spend_cashback: bool
    need_account: bool
    bill_email: str
    remember_account: bool
    email: str
    password: str
    promo_code: str
    
    def get_promo_code_discount(self) -> int | None:
        discount = utils.check_promo_code(self.promo_code)
        if not discount:
            self.promo_code = None
            discount = 0
        return discount
    
    def get_amount(self, promo_code_discount: int = None) -> int:
        amount = self.cart.aggregate(Sum('final_price')).get('final_price__sum')
        if promo_code_discount:
            amount -= amount * promo_code_discount / 100
        if self.spend_cashback:
            if self.profile.cashback >= amount:
                return 1
            amount -= self.profile.cashback
        return amount
    
    def get_description(self, publication: models.ProductPublication) -> str:
        description = f'{publication.title}'
        for platform in publication.platforms.all():
            description += f' - {platform.name}'
        return description
    
    def remember_ps_account(self):
        self.profile.playstation_email = self.email
        self.profile.playstation_password = self.password
        self.profile.bill_email = self.bill_email
        self.profile.save()
    
    def fill_order(self, order: models.Order, promo_code_discount: int) -> models.Order:
        if self.remember_account:
            self.remember_ps_account()
        order.cashback = 0
        for publication in self.cart:
            if not self.spend_cashback:
                order.cashback += publication.final_price * publication.cashback / 100
            models.OrderProduct.objects.get_or_create(
                order=order,
                product=publication.product.title,
                product_id=publication.id,
                description=self.get_description(publication),
                original_price=publication.original_price,
                final_price=publication.final_price,
            )
        if order.promo_code_discount:
            order.cashback -= order.cashback * promo_code_discount / 100
        payment = serializers.PaymentSerializer(
            data=requests.post(f'{PAYMENTS_URL}/create_payment', json={
                'order_id': str(order.id),
                'amount': order.amount,
                'description': str(order),
                'customer_telegram_id': order.profile.telegram_id,
            }).json()
        )
        if payment.is_valid():
            order.payment_id = payment.validated_data.get('payment_id')
            order.payment_url = payment.validated_data.get('payment_url')
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
            status=models.Order.StatusChoices.CREATED,
            promo_code=self.promo_code,
            promo_code_discount=promo_code_discount,
        )
        if created:
            order = self.fill_order(order, promo_code_discount)
        return order


class CreateOrder(APIView):
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        order_info = OrderInfo(
            profile,
            models.ProductPublication.objects.filter(id__in=request.data.get('cart', [])),
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
            models.ChatMessage.objects.create(
                order=order,
                text=text,
                manager=request.user if request.user.id else None,
            )
            if request.user.id:
                requests.post(
                    f'http://{os.environ.get("TELEGRAM_BOT_HOST")}:{os.environ.get("TELEGRAM_BOT_PORT")}/api/order/message/send/',
                    json={
                        'user_id': order.profile.telegram_id,
                        'order_id': order_id,
                        'text': text
                    }
                )
                return Response(status=status.HTTP_200_OK)
            return Response(
                serializers.ChatMessageSerializer(
                    models.ChatMessage.objects.filter(order=order),
                    many=True,
                ).data,
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatus(APIView):
    def post(self, request: Request):
        check_token = requests.post(PAYMENTS_URL+'/check_token', json=request.data).json()
        if check_token.get('TokenCorrect'):
            order = models.Order.objects.filter(id=request.data.get('OrderId')).first()
            if order:
                if request.data.get('Status') == 'CONFIRMED':
                    async_to_sync(send_admin_notification)({'text': f'Заказ {order.id} оплачен',
                                                            'level': NotifyLevels.SUCCESS.value})
                    order.status = models.Order.StatusChoices.PAID
                    bot_url = f'http://{os.environ.get("TELEGRAM_BOT_HOST")}:{os.environ.get("TELEGRAM_BOT_PORT")}/api/order/payment/access/'
                    requests.post(bot_url, data={'user_id': order.profile.id,
                                                 'order_id': order.id,
                                                 'need_account': order.need_account})
                else:
                    async_to_sync(send_admin_notification)({'text': f'Заказ {order.id} не был оплачен за выделенное время',
                                                            'level': NotifyLevels.ERROR.value})
                    order.status = models.Order.StatusChoices.ERROR
                order.save()
            return Response('OK')
        return Response(status=status.HTTP_400_BAD_REQUEST)
