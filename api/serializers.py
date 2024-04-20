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
