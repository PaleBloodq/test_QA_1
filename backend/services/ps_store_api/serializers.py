import logging
from urllib.parse import quote
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        return super().to_internal_value(datetime.fromtimestamp(float(f'{value}') / 1000))


class URLField(serializers.URLField):
    def to_internal_value(self, data):
        return super().to_internal_value(quote(data, '/:?&='))


@dataclass
class Price:
    base_price: Optional[Decimal]
    discounted_price: Optional[Decimal]
    discount: int
    discount_deadline: datetime
    
    @staticmethod
    def _normalize_price(price: int) -> Optional[Decimal]:
        try:
            return Decimal(price) / Decimal(100)
        except:
            return None
    
    @staticmethod
    def _normalize_discount(discount: str) -> int:
        try:
            return int(discount.replace('-', '').replace('%', ''))
        except:
            return 0
    
    def __post_init__(self):
        self.base_price = self._normalize_price(self.base_price)
        self.discounted_price = self._normalize_price(self.discounted_price)
        self.discount = self._normalize_discount(self.discount)


@dataclass
class Edition:
    id: str
    name: str
    price: Price
    ps_plus_price: Price
    platforms: list[str]
    image: Optional[str]
    release_date: datetime
    
    def __post_init__(self):
        self.price = Price(**self.price)
        self.ps_plus_price = Price(**self.ps_plus_price)


class PriceSerializer(serializers.Serializer):
    basePriceValue = serializers.IntegerField(source='base_price', allow_null=True)
    discountedValue = serializers.IntegerField(source='discounted_price', allow_null=True)
    discountText = serializers.CharField(source='discount', allow_null=True)
    endTime = TimestampField(source='discount_deadline', allow_null=True)


class EditionSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, allow_blank=True)


class MediaSerializer(serializers.Serializer):
    role = serializers.CharField()
    type = serializers.CharField()
    url = URLField()


class MobilectasSerializer(serializers.Serializer):
    type = serializers.CharField()
    price = PriceSerializer()


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    edition = EditionSerializer(allow_null=True)
    media = MediaSerializer(source='image', many=True)
    platforms = serializers.ListField(child=serializers.CharField())
    releaseDate = serializers.DateTimeField(source='release_date')
    mobilectas = MobilectasSerializer(many=True)
    
    def _get_image(self, media_list: list[dict]) -> str:
        image = None
        for media_ in media_list:
            type = media_.get('type')
            role = media_.get('role')
            if (type == 'IMAGE' and (role == 'PORTRAIT_BANNER' or (role == 'MASTER' and image is None))):
                image = media_.get('url')
        return image
    
    def _get_name(self, edition: Optional[dict], name: Optional[str]) -> str:
        if edition:
            edition_name = edition.get('name')
            if edition_name:
                return edition_name
        return name
    
    def _get_price(self, mobilectas: list[dict], tag: str) -> dict:
        for mobilecta in mobilectas:
            if mobilecta.get('type') == tag:
                return mobilecta.get('price')
        return {
            'base_price': None,
            'discounted_price': None,
            'discount': None,
            'discount_deadline': None,
        }
    
    def create(self, validated_data: dict) -> Edition:
        validated_data['name'] = self._get_name(validated_data.pop('edition'), validated_data['name'])
        validated_data['image'] = self._get_image(validated_data['image'])
        mobilectas = validated_data.pop('mobilectas')
        validated_data['ps_plus_price'] = self._get_price(mobilectas, 'UPSELL_PS_PLUS_DISCOUNT')
        validated_data['price'] = self._get_price(mobilectas, 'ADD_TO_CART')
        return Edition(**validated_data)
