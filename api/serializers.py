from rest_framework import serializers
from api import models


class EnumSerializer(serializers.RelatedField):
    def to_representation(self, value: models.EnumBaseModel):
        return value.name
    

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = (
            'id',
            'name',
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = (
            'id',
            'name',
        )

class ProductPublicationSerializer(serializers.ModelSerializer):
    platforms = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'price',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'preview',
            'photo',
            'cashback',
            'ps_plus_discount',
            'discount',
            'discount_deadline',
        )


class ProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    publications = ProductPublicationSerializer(many=True)
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'languages',
            'release_date',
            'publications',
        )


class SingleProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'languages',
            'release_date',
        )


class SingleProductPublicationSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer()
    platforms = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'price',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'preview',
            'photo',
            'cashback',
            'ps_plus_discount',
            'discount',
            'discount_deadline',
            'product',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = (
            'playstation_email',
            'playstation_password',
            'bill_email',
            'cashback',
        )


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = (
            'item',
            'description',
            'price',
        )


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    
    class Meta:
        model = models.Order
        fields = (
            'date',
            'amount',
            'status',
            'order_products',
        )
