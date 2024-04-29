from datetime import datetime, date
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
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


class UpdateProductPublications(APIView):
    def post(self, request: Request, product_id: str):
        product = models.Product.objects.filter(id=product_id).first()
        if product:
            for publication in request.data.get('publications', []):
                serializer = serializers.UpdateProductPublicationSerializer(
                    data=publication,
                    instance=None,
                )
                if serializer.is_valid():
                    serializer.save(product)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
