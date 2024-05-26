import logging
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
    base_price: Decimal
    discounted_price: Decimal
    discount: int
    discount_deadline: datetime


@dataclass
class Edition:
    id: str
    name: str
    price: Price
    platforms: list[str]
    image: str
    release_date: datetime


class Data(serializers.Serializer):
    conceptRetrieve = ConceptRetrieveSerializer(required=False)
    productRetrieve = ProductRetrieveSerializer(required=False)
    
    @staticmethod
    def _normalize_discount(discount: str) -> int:
        try:
            return int(discount.replace('-', '').replace('%', ''))
        except:
            return 0
    
    @staticmethod
    def _get_image(media: list[dict]) -> str:
        for media_ in media:
            if media_.get('type') == 'IMAGE' and media_.get('role') == 'PORTRAIT_BANNER':
                return media_.get('url')
        return ''
    
    def get_editions(self) -> list[Edition]:
        concept = self.validated_data.get('conceptRetrieve')
        if concept is None:
            concept = self.validated_data.get('productRetrieve').get('concept')
        editions = concept.get('selectableProducts').get('purchasableProducts')
        logging.warning(editions)
        return [
            Edition(
                edition.get('id'),
                edition.get('edition').get('name') or edition.get('name'),
                Price(
                    Decimal(edition.get('price').get('basePriceValue')) / Decimal(100),
                    Decimal(edition.get('price').get('discountedValue')) / Decimal(100),
                    self._normalize_discount(edition.get('price').get('discountText')),
                    edition.get('price').get('endTime'),
                ),
                edition.get('platforms'),
                self._get_image(edition.get('media')),
                edition.get('releaseDate'),
            )
            for edition in editions
        ]
