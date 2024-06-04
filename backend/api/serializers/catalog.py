from rest_framework import serializers
from api import models


__all__ = [
    'EnumSerializer',
    'PlatformSerializer',
    'LanguageSerializer',
    'ProductPublicationSerializer',
    'ProductSerializer',
    'SingleProductSerializer',
    'SingleProductPublicationSerializer',
]


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
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'final_price',
            'discount',
            'discount_deadline',
            'ps_plus_final_price',
            'ps_plus_discount',
            'ps_plus_discount_deadline',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'product_page_image',
            'search_image',
            'offer_image',
            'cashback',
            'is_main',
            'languages',
        )


class ProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    publications = ProductPublicationSerializer(many=True)
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'release_date',
            'publications',
        )


class SingleProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    
    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'type',
            'release_date',
        )


class SingleProductPublicationSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer()
    platforms = EnumSerializer(many=True, read_only=True)
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'title',
            'final_price',
            'discount',
            'discount_deadline',
            'ps_plus_final_price',
            'ps_plus_discount',
            'ps_plus_discount_deadline',
            'duration',
            'quantity',
            'includes',
            'platforms',
            'product_page_image',
            'search_image',
            'offer_image',
            'cashback',
            'product',
            'languages',
        )
