from rest_framework import serializers
from api import models


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = (
            'id',
            'name',
        )


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = (
            'id',
            'name',
        )


class ProductPublicationSerializer(serializers.ModelSerializer):
    platform = serializers.CharField()
    language = serializers.CharField()
    
    class Meta:
        model = models.ProductPublication
        fields = (
            'id',
            'platform',
            'language',
            'title',
            'price',
            'preview',
            'photo',
            'includes',
            'cashback',
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
