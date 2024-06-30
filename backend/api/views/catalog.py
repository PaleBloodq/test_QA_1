import logging

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from api import models, serializers
from api.cache_api import CacheProxy


class GetCategories(APIView):
    def get(self, request: Request):
        return Response(self.get_categories())

    @staticmethod
    @CacheProxy.memoize(timeout=3600, depend_models=[
        models.Product, models.Tag, models.Publication,
        models.AddOn, models.Subscription])
    def get_categories():
        return [
            {
                'tag': tag.database_name,
                'name': tag.name,
                'objects': serializers.ProductSerializer(
                    tag.products.all(),
                    many=True,
                ).data,
            } for tag in models.Tag.objects.all()]


class GetProduct(APIView):
    def get(self, request: Request, product_id: str):
        response = serializers.ProductSerializer(
            models.Product.objects.get(id=product_id)
        ).data
        return Response(response)


class GetPublication(APIView):
    def get(self, request: Request, type: str, publication_id: str):
        model, serializer = {
            'publication': (models.Publication, serializers.PublicationWithProductSerializer),
            'add_on': (models.AddOn, serializers.AddOnWithProductSerializer),
            'subscription': (models.Subscription, serializers.SubscriptionWithProductSerializer)
        }.get(type)
        return Response(serializer(model.objects.get(id=publication_id)).data)


class GetFilters(APIView):
    def get(self, request: Request):
        return Response(self.get_filters())

    @staticmethod
    @CacheProxy.memoize(
        timeout=3600, depend_models=[
        models.Platform, models.Language, models.Publication,
        models.AddOn, models.Subscription])
    def get_filters():
        def final_price(model, reverse: bool) -> int:
            try:
                return model.objects.latest(f'{"-" if reverse else ""}final_price').final_price
            except:
                return 1_000_000 if reverse else 0
        return {
            'platforms': serializers.PlatformSerializer(
                models.Platform.objects.all(),
                many=True,
            ).data,
            'languages': serializers.LanguageSerializer(
                models.Language.objects.all(),
                many=True,
            ).data,
            'minPrice': min(
                final_price(models.Publication, True),
                final_price(models.AddOn, True),
                final_price(models.Subscription, True),
            ),
            'maxPrice': max(
                final_price(models.Publication, False),
                final_price(models.AddOn, False),
                final_price(models.Subscription, False),
            ),
        }


class SearchProducts(APIView):
    def post(self, request: Request):
        offset = request.data.get('offset', 0)
        limit = request.data.get('limit', 20)
        query = {}
        if request.data.get('minPrice'):
            query['final_price__gte'] = request.data.get('minPrice')
        if request.data.get('maxPrice'):
            query['final_price__lte'] = request.data.get('maxPrice')
        if request.data.get('platforms'):
            query['platforms__in'] = request.data.get('platforms')
        if request.data.get('languages'):
            query['languages__in'] = request.data.get('languages')
        if request.data.get('q'):
            query['product__title__iregex'] = request.data.get('q')
        def instances(model):
            if query:
                return model.objects.filter(**query).distinct()[offset:limit]
            return model.objects.all()[offset:limit]
        return Response({
            'publications': serializers.PublicationWithProductSerializer(
                instances(models.Publication),
                many=True
            ).data,
            'add_ons': serializers.AddOnWithProductSerializer(
                instances(models.AddOn),
                many=True
            ).data,
            'subscriptions': serializers.SubscriptionWithProductSerializer(
                instances(models.Subscription),
                many=True
            ).data,
        })
