from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.exceptions import ValidationError
from .. import utils, models, serializers


__all__ = [
    'Cart',
]


class Cart(APIView):
    def get_product_publication(self, id) -> models.AbstractProductPublication:
        result = models.Publication.objects.filter(id=id).first()
        if result is None:
            result = models.AddOn.objects.filter(id=id).first()
        if result is None:
            result = models.Subscription.objects.filter(id=id).first()
        if result is None:
            raise ValidationError({'error': 'Товар не найден'})
        return result
    
    @utils.auth_required
    def get(self, request: Request, profile: models.Profile):
        cart = models.Cart.objects.get_or_create(profile=profile)[0]
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        serializer = serializers.ChangeCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = models.Cart.objects.get_or_create(profile=profile)[0]
        product = self.get_product_publication(serializer.validated_data.get('id'))
        match product.typename:
            case 'publication':
                cart.publications.add(product)
            case 'add_on':
                cart.add_ons.add(product)
            case 'subscription':
                cart.subscriptions.add(product)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    
    @utils.auth_required
    def delete(self, request: Request, profile: models.Profile):
        serializer = serializers.ChangeCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = models.Cart.objects.get_or_create(profile=profile)[0]
        product = self.get_product_publication(serializer.validated_data.get('id'))
        match product.typename:
            case 'publication':
                cart.publications.remove(product)
            case 'add_on':
                cart.add_ons.remove(product)
            case 'subscription':
                cart.subscriptions.remove(product)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
