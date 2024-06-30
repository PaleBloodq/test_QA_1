from rest_framework import serializers
from .. import models


__all__ = [
    'PlatformSerializer',
    'LanguageSerializer',
    'PublicationSerializer',
    'PublicationWithProductSerializer',
    'AddOnSerializer',
    'AddOnWithProductSerializer',
    'SubscriptionSerializer',
    'SubscriptionWithProductSerializer',
    'ProductSerializer',
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


class PublicationSerializer(serializers.ModelSerializer):
    platforms = EnumSerializer(many=True, read_only=True)
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Publication
        fields = [
            'id',
            'product_type',
            'is_main',
            'platforms',
            'final_price',
            'discount',
            'discount_deadline',
            'ps_plus_final_price',
            'ps_plus_discount',
            'ps_plus_discount_deadline',
            'languages',
            'title',
            'includes',
            'product_page_image',
            'search_image',
            'offer_image',
            'cashback',
            'release_date',
        ]


class AddOnSerializer(serializers.ModelSerializer):
    platforms = EnumSerializer(many=True, read_only=True)
    languages = EnumSerializer(many=True, read_only=True)
    type = serializers.SlugRelatedField('name', read_only=True)
    
    class Meta:
        model = models.AddOn
        fields = [
            'id',
            'product_type',
            'is_main',
            'platforms',
            'final_price',
            'discount',
            'discount_deadline',
            'ps_plus_final_price',
            'ps_plus_discount',
            'ps_plus_discount_deadline',
            'languages',
            'title',
            'includes',
            'product_page_image',
            'search_image',
            'offer_image',
            'cashback',
            'type',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    platforms = EnumSerializer(many=True, read_only=True)
    languages = EnumSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Subscription
        fields = [
            'id',
            'product_type',
            'is_main',
            'platforms',
            'final_price',
            'discount',
            'discount_deadline',
            'ps_plus_final_price',
            'ps_plus_discount',
            'ps_plus_discount_deadline',
            'languages',
            'title',
            'includes',
            'product_page_image',
            'search_image',
            'offer_image',
            'cashback',
            'duration',
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    
    class Meta:
        model = models.Product
        fields = [
            'id',
            'title',
            'type',
            'release_date',
        ]


class PublicationWithProductSerializer(PublicationSerializer):
    product = SimpleProductSerializer()
    
    class Meta(PublicationSerializer.Meta):
        fields = PublicationSerializer.Meta.fields + [
            'product'
        ]


class AddOnWithProductSerializer(AddOnSerializer):
    product = SimpleProductSerializer()
    
    class Meta(AddOnSerializer.Meta):
        fields = AddOnSerializer.Meta.fields + [
            'product'
        ]


class SubscriptionWithProductSerializer(SubscriptionSerializer):
    product = SimpleProductSerializer()
    
    class Meta(SubscriptionSerializer.Meta):
        fields = SubscriptionSerializer.Meta.fields + [
            'product'
        ]


class ProductSerializer(SimpleProductSerializer):
    publications = PublicationSerializer(source='api_publication_related', many=True)
    add_ons = AddOnSerializer(source='api_addon_related', many=True)
    subscriptions = SubscriptionSerializer(source='api_subscription_related', many=True)
    
    class Meta(SimpleProductSerializer.Meta):
        fields = SimpleProductSerializer.Meta.fields + [
            'publications',
            'add_ons',
            'subscriptions',
        ]
