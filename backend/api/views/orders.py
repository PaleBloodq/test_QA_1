from datetime import datetime, date
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from api import models, serializers, utils


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
        try:
            publications = models.ProductPublication.objects.filter(
                id__in=request.data.get('cart', [])
            )
            amount = publications.aggregate(Sum('final_price')).get('final_price__sum')
            promo = utils.check_promo_code(request.data.get('promoCode'))
            if promo:
                amount = int(amount * promo / 100)
            order, created = models.Order.objects.get_or_create(
                profile=profile,
                date=date.today(),
                amount=amount,
            )
            if created:
                cashback = 0
                for publication in publications:
                    cashback += publication.final_price * publication.cashback / 100
                    models.OrderProduct.objects.get_or_create(
                        order=order,
                        product=publication.product.title,
                        product_id=publication.id,
                        description=self.get_description(publication),
                        original_price=publication.original_price,
                        final_price=publication.final_price,
                    )
                if request.data.get('hasAccount'):
                    order.email = profile.playstation_email
                    order.password = profile.playstation_password
                else:
                    order.email = request.data.get('accountEmail')
                    order.password = request.data.get('accountPassword')
                order.cashback = int(cashback)
                order.status = models.Order.StatusChoices.CREATED
                order.bill_email = request.data.get('billEmail')
                order.spend_cashback = bool(request.data.get('spendCashback'))
                order.save()
                if request.data.get('rememberAccount'):
                    profile.playstation_email = order.email
                    profile.playstation_password = order.password
                    profile.bill_email = order.bill_email
                    profile.save()
            return Response(status=status.HTTP_200_OK)
        except:
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
