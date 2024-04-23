from datetime import datetime
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api import models, serializers, utils


class GetCategories(APIView):
    def get(self, request: Request):
        response = [
            {
                'tag': tag.database_name,
                'name': tag.name,
                'objects': serializers.ProductSerializer(
                    tag.products.all(),
                    many=True,
                ).data,
            } for tag in models.Tag.objects.all()]
        return Response(response)


class GetProduct(APIView):
    def get(self, request: Request, product_id: str):
        response = serializers.ProductSerializer(
            models.Product.objects.get(id=product_id)
        ).data
        return Response(response)


class GetPublication(APIView):
    def get(self, request: Request, publication_id: str):
        response = serializers.SingleProductPublicationSerializer(
            models.ProductPublication.objects.get(id=publication_id)
        ).data
        return Response(response)


class GetFilters(APIView):
    def get(self, request: Request):
        response = {
            'platforms': serializers.PlatformSerializer(
                models.Platform.objects.all(),
                many=True,
            ).data,
            'languages': serializers.LanguageSerializer(
                models.Language.objects.all(),
                many=True,
            ).data,
            'minPrice': models.ProductPublication.objects.latest('-price').price,
            'maxPrice': models.ProductPublication.objects.latest('price').price,
        }
        return Response(response)


class SearchProducts(APIView):
    def post(self, request: Request):
        offset = request.data.get('offset', 0)
        limit = request.data.get('limit', 20)
        query = {}
        if request.data.get('minPrice'):
            query['price__gte'] = request.data.get('minPrice')
        if request.data.get('maxPrice'):
            query['price__lte'] = request.data.get('maxPrice')
        if request.data.get('platforms'):
            query['platforms__in'] = request.data.get('platforms')
        if request.data.get('languages'):
            query['product__languages__in'] = request.data.get('languages')
        if request.data.get('q'):
            query['product__title__iregex'] = request.data.get('q')
        if query:
            instance = models.ProductPublication.objects.filter(**query).distinct()[offset:limit]
        else:
            instance = models.ProductPublication.objects.all()[offset:limit]
        response = serializers.SingleProductPublicationSerializer(
            instance,
            many=True,
        ).data
        return Response(response)


class GetToken(APIView):
    def post(self, request: Request):
        telegram_id = request.data.get('telegram_id')
        if telegram_id:
            return Response({
                'token': utils.encode_profile(telegram_id)
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    def post(self, request: Request):
        token = request.data.get('token')
        if token:
            profile = utils.decode_token(token)
            if profile:
                return Response({
                    'token': utils.encode_profile(profile.telegram_id)
                }, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    def post(self, request: Request):
        token = request.data.get('token')
        if token:
            if utils.decode_token(token):
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    @utils.auth_required
    def get(self, request: Request, profile: models.Profile):
        response = serializers.ProfileSerializer(profile).data
        return Response(response)


class UpdateProfile(APIView):
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        if request.data.get('psEmail'):
            profile.playstation_email = request.data.get('psEmail')
        if request.data.get('psPassword'):
            profile.playstation_password = request.data.get('psPassword')
        if request.data.get('billEmail'):
            profile.bill_email = request.data.get('billEmail')
        try:
            profile.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = serializers.ProfileSerializer(profile).data
        return Response(response)


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
            promo_code = models.PromoCode.objects.filter(
                promo_code=promo_code,
                expiration__gte=datetime.now()
            )
            if promo_code:
                return Response({
                    'result': True,
                    'discount': promo_code.get().discount
                })
            return Response({'result': False})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateOrder(APIView):
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        return Response(status=status.HTTP_200_OK)
