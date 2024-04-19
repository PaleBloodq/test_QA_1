from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from api import models, serializers


class GetCategories(APIView):
    def create_static_data(self):
        models.Type.objects.get_or_create(name='subscription')
        models.Type.objects.get_or_create(name='game')
        models.Tag.objects.get_or_create(name='Подписки EA Play', database_name='eaPlay')
        models.Tag.objects.get_or_create(name='Подписки PS Plus', database_name='psPlus')
        models.Tag.objects.get_or_create(name='Офферы', database_name='offers')
        models.Tag.objects.get_or_create(name='Новинки', database_name='new')
        models.Tag.objects.get_or_create(name='Лидеры продаж', database_name='leaders')
    
    def get(self, request: Request):
        self.create_static_data()
        response = [
            {
                'tag': tag.database_name,
                'name': tag.name,
                'objects': serializers.ProductSerializer(
                    models.Product.objects.filter(tag__tag=tag),
                    many=True,
                ).data
            } for tag in models.Tag.objects.all()]
        response.append({
            'tag': 'donations',
            'name': 'Игровой донат',
            'objects': serializers.DonationSerializer(
                models.Donation.objects.all(),
                many=True,
            ).data
        })
        return Response(response)
