import logging
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
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
                'products': serializers.ProductSerializer(
                    tag.products.all(),
                    many=True,
                ).data,
                'publications': serializers.PublicationWithProductSerializer(
                    tag.publications.all(),
                    many=True,
                ).data,
                'add_ons': serializers.AddOnWithProductSerializer(
                    tag.add_ons.all(),
                    many=True,
                ).data,
                'subscriptions': serializers.SubscriptionWithProductSerializer(
                    tag.subscriptions.all(),
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
        serializer = serializers.SearchProductsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_response())
