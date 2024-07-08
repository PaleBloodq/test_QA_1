import re
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
    'SearchProductsSerializer',
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


class SearchProductsSerializer(serializers.Serializer):
    minPrice = serializers.IntegerField(required=False)
    maxPrice = serializers.IntegerField(required=False)
    platforms = serializers.ListField(
        required=False,
        child=serializers.UUIDField()
    )
    languages = serializers.ListField(
        required=False,
        child=serializers.UUIDField()
    )
    q = serializers.CharField(required=False, allow_blank=True)
    offset = serializers.IntegerField(required=False, default=0)
    limit = serializers.IntegerField(required=False, default=20)
    typename = serializers.ChoiceField([
        'publication', 'add_on', 'subscription'
    ])
    
    def get_serializer_by_typename(self) -> PublicationSerializer:
        return {
            'publication': PublicationWithProductSerializer,
            'add_on': AddOnWithProductSerializer,
            'subscription': SubscriptionWithProductSerializer,
        }.get(self.validated_data.get('typename'))
    
    def get_query(self) -> dict:
        query = {}
        if self.validated_data.get('minPrice'):
            query['final_price__gte'] = self.validated_data.get('minPrice')
        if self.validated_data.get('maxPrice'):
            query['final_price__lte'] = self.validated_data.get('maxPrice')
        if self.validated_data.get('platforms'):
            query['platforms__in'] = self.validated_data.get('platforms')
        if self.validated_data.get('languages'):
            query['languages__in'] = self.validated_data.get('languages')
        if self.validated_data.get('q'):
            q_words = [re.escape(n) for n in re.sub(r'\W+', ' ', self.validated_data.get('q')).lower().split(' ')]
            q_clean = r'(' + '.*' + '.*|.*'.join(q_words) + '.*' + ')'
            query['product__title__iregex'] = q_clean
        return query
    
    def get_instances(self, model, query: dict, limit: int, offset: int):
        if query:
            instances = model.objects.filter(**query).distinct()
        else:
            instances = model.objects.all()
        return instances.order_by('-discount')[offset:limit]

    def get_response(self) -> dict:
        serializer = self.get_serializer_by_typename()
        return serializer(
            self.get_instances(
                serializer.Meta.model,
                self.get_query(),
                self.validated_data.get('limit'),
                self.validated_data.get('offset'),
            ), many=True
        ).data
