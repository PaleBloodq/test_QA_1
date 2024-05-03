import os
from datetime import date
import requests
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from api import models, serializers, utils

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


class CreateOrder(APIView):
    def get_description(self, publication: models.ProductPublication) -> str:
        description = f'{publication.title}'
        for platform in publication.platforms.all():
            description += f' - {platform.name}'
        return description
    
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        cart = models.ProductPublication.objects.filter(
            id__in=request.data.get('cart', [])
        )
        spend_cashback: bool = request.data.get('spendCashback', False)
        email = request.data.get('accountEmail', profile.playstation_email)
        password = request.data.get('accountPassword', profile.playstation_password)
        bill_email = request.data.get('billEmail', profile.bill_email)
        promo_code = request.data.get('promoCode')
        promo_code_discount = utils.check_promo_code(promo_code)
        remember_account: bool = request.data.get('rememberAccount', False)
        if cart and email and password and bill_email:
            amount = cart.aggregate(Sum('final_price')).get('final_price__sum')
            if promo_code_discount:
                amount -= amount * promo_code_discount / 100
            order, order_created = models.Order.objects.get_or_create(
                profile=profile,
                date=date.today(),
                amount=amount,
                email=email,
                password=password,
                bill_email=bill_email,
                spend_cashback=spend_cashback,
                status=models.Order.StatusChoices.CREATED,
                promo_code=promo_code,
                promo_code_discount=promo_code_discount,
            )
            if order_created:
                if remember_account:
                    profile.playstation_email = email
                    profile.playstation_password = password
                    profile.bill_email = bill_email
                    profile.save()
                order.cashback = 0
                for publication in cart:
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
                        'customer_telegram_id': profile.telegram_id,
                    }).json()
                )
                if payment.is_valid():
                    order.payment_id = payment.validated_data.get('payment_id')
                    order.payment_url = payment.validated_data.get('payment_url')
                order.save()
            return Response(
                {
                    'PaymentUrl': order.payment_url
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatMessages(APIView):
    def post(self, request: Request):
        order_id = request.data.get('order_id')
        text = request.data.get('text')
        if order_id and text:
            order = models.Order.objects.get(id=order_id)
            models.ChatMessage.objects.create(
                order=order,
                text=text
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatus(APIView):
    def post(self, request: Request):
        check_token = requests.post(PAYMENTS_URL+'/check_token', json=request.data).json()
        if check_token.get('TokenCorrect'):
            order = models.Order.objects.filter(id=request.data.get('OrderId')).first()
            if order:
                if request.data.get('Status') == 'CONFIRMED':
                    order.status = models.Order.StatusChoices.PAID
                else:
                    order.status = models.Order.StatusChoices.ERROR
                order.save()
            return Response('OK')
        return Response(status=status.HTTP_400_BAD_REQUEST)
