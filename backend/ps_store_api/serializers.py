from urllib.parse import quote
from decimal import Decimal
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models


class ReleaseDateField(serializers.DateTimeField):
    def to_internal_value(self, value: dict):
        return super().to_internal_value(value.get('value'))


class TimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        return super().to_internal_value(datetime.fromtimestamp(float(f'{value}') / 1000))


class MediaField(serializers.URLField):
    def to_internal_value(self, data: list[dict]):
        for media in data:
            if media.get('type') == 'IMAGE' and media.get('role') == 'PORTRAIT_BANNER':
                return super().to_internal_value(quote(media.get('url'), '/:?&='))
        for media in data:
            if media.get('type') == 'IMAGE' and media.get('role') == 'MASTER':
                return super().to_internal_value(quote(media.get('url'), '/:?&='))


class DiscountField(serializers.IntegerField):
    def to_internal_value(self, data: str):
        try:
            discount = int(data.replace('-', '').replace('%', ''))
        except:
            discount = 0
        return super().to_internal_value(discount)


class PriceField(serializers.DecimalField):
    def to_internal_value(self, data: int):
        return super().to_internal_value(Decimal(data) / Decimal(100))


class ConceptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    releaseDate = ReleaseDateField(source='release_date')
    publisherName = serializers.CharField(source='publisher_name')
    
    def create(self, validated_data):
        return models.Concept.objects.create(**validated_data)
    
    def update(self, instance: models.Concept, validated_data):
        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance
    
    class Meta:
        fields = [
            'id',
            'name',
            'releaseDate',
            'publisherName',
        ]


class PriceSerializer(serializers.Serializer):
    basePriceValue = PriceField(source='base_price', max_digits=10, decimal_places=2)
    discountedValue = PriceField(source='discounted_price', max_digits=10, decimal_places=2)
    endTime = TimestampField(source='discount_deadline', allow_null=True)
    isFree = serializers.BooleanField(source='is_free')
    discountText = DiscountField(source='discount', allow_null=True)
    
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if value.get('discount') is None:
            value['discount'] = 0
        return value
    
    class Meta:
        fields = [
            'basePriceValue',
            'discountedValue',
            'endTime',
            'isFree',
            'discountText',
        ]


class MobilectaSerializer(serializers.Serializer):
    type = serializers.CharField()
    price = PriceSerializer()
    
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        value.update(**value.pop('price'))
        return value
    
    class Meta:
        fields = [
            'type',
            'price',
        ]


class MobilectasField(serializers.ListField):
    child = MobilectaSerializer()
    
    def to_internal_value(self, data):
        values = []
        for value in super().to_internal_value(data):
            if not value.pop('is_free'):
                values.append(value)
        return values


class AbstractProductSerializer(serializers.Serializer):
    model = models.AbstractProduct
    id = serializers.CharField()
    name = serializers.CharField()
    platforms = serializers.ListField(
        child=serializers.CharField()
    )
    media = MediaField(source='portrait_image')
    mobilectas = MobilectasField()
    
    price_fields = {
        'ADD_TO_CART': 'price',
        'UPSELL_PS_PLUS_DISCOUNT': 'ps_plus_price'
    }
    
    def validate(self, attrs: dict) -> dict:
        if attrs.get('price') is None:
            raise ValidationError('Price not found')
        return attrs
    
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        for mobilecta in value.pop('mobilectas'):
            field = self.price_fields.get(mobilecta.get('type'))
            if field:
                value[field] = mobilecta
        return value
    
    def create(self, validated_data: dict):
        price = validated_data.get('price')
        if price:
            validated_data['price'] = models.Mobilecta.objects.create(**price)
        ps_plus_price = validated_data.get('ps_plus_price')
        if ps_plus_price:
            validated_data['ps_plus_price'] = models.Mobilecta.objects.create(**ps_plus_price)
        platforms = validated_data.pop('platforms', [])
        instance = self.model.objects.create(**validated_data)
        for platform in platforms:
            instance.platforms.add(
                models.Platform.objects.get_or_create(name=platform)[0]
            )
        return instance
    
    def update(self, instance: models.AbstractProduct, validated_data):
        if instance.price:
            instance.price.delete()
        price = validated_data.get('price')
        if price:
            instance.price = models.Mobilecta.objects.create(**price)
        if instance.ps_plus_price:
            instance.ps_plus_price.delete()
        ps_plus_price = validated_data.get('ps_plus_price')
        if ps_plus_price:
            instance.ps_plus_price = models.Mobilecta.objects.create(**ps_plus_price)
        instance.save()
        return instance


class ProductSerializer(AbstractProductSerializer):
    model = models.Product
    npTitleId = serializers.CharField(source='np_title_id')
    releaseDate = serializers.DateTimeField(source='release_date')
    
    class Meta:
        fields = [
            'id',
            'npTitleId',
            'name',
            'platforms',
            'releaseDate',
            'media',
            'mobilectas',
        ]


class AddOnSerializer(AbstractProductSerializer):
    model = models.AddOn
    
    class Meta:
        fields = [
            'id',
            'name',
            'platforms',
            'media',
            'mobilectas',
        ]
