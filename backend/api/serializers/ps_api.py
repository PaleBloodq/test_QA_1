import logging
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        return super().to_internal_value(datetime.fromtimestamp(float(f'{value}') / 1000))


class PriceSerializer(serializers.Serializer):
    basePriceValue = serializers.IntegerField(allow_null=True)
    discountedValue = serializers.IntegerField(allow_null=True)
    discountText = serializers.CharField(allow_null=True)
    endTime = TimestampField(allow_null=True)


class EditionSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True, allow_blank=True)


class MediaSerializer(serializers.Serializer):
    role = serializers.CharField()
    type = serializers.CharField()
    url = serializers.URLField()


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    price = PriceSerializer()
    edition = EditionSerializer()
    media = MediaSerializer(many=True)
    platforms = serializers.ListField(child=serializers.CharField())
    releaseDate = serializers.DateTimeField()


class SelectableProductsSerializer(serializers.Serializer):
    purchasableProducts = ProductSerializer(many=True)


class ConceptRetrieveSerializer(serializers.Serializer):
    selectableProducts = SelectableProductsSerializer()


class ProductRetrieveSerializer(serializers.Serializer):
    concept = ConceptRetrieveSerializer()


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
    platforms: list[str]
    image: Optional[str]
    release_date: datetime
    
    @staticmethod
    def _get_image(media: list[dict]) -> str:
        for media_ in media:
            if media_.get('type') == 'IMAGE' and media_.get('role') == 'PORTRAIT_BANNER':
                return media_.get('url')
        return ''
    
    def __post_init__(self):
        self.image = self._get_image(self.image)


class Data(serializers.Serializer):
    conceptRetrieve = ConceptRetrieveSerializer(required=False)
    productRetrieve = ProductRetrieveSerializer(required=False)
    
    def get_editions(self) -> list[Edition]:
        concept = self.validated_data.get('conceptRetrieve')
        if concept is None:
            concept = self.validated_data.get('productRetrieve').get('concept')
        editions_list = concept.get('selectableProducts').get('purchasableProducts')
        editions = []
        for edition in editions_list:
            price = Price(
                edition.get('price').get('basePriceValue'),
                edition.get('price').get('discountedValue'),
                edition.get('price').get('discountText'),
                edition.get('price').get('endTime'),
            )
            if price.base_price is None or price.discounted_price is None:
                continue
            editions.append(
                Edition(
                    edition.get('id'),
                    edition.get('edition').get('name') or edition.get('name'),
                    price,
                    edition.get('platforms'),
                    edition.get('media'),
                    edition.get('releaseDate'),
                )
            )
        logging.info(f'{len(editions)} editions found.')
        return editions
