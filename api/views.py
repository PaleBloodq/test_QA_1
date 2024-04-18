from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from api import models, serializers


class GetCategories(APIView):
    def get(self, request: Request):
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
