from asgiref.sync import async_to_sync
from rest_framework import serializers
from api import models, utils
from api.senders import send_admin_notification, NotifyLevels


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
            'final_price',
            'original_price',
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
            'final_price',
            'original_price',
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


class UpdateProductPublicationSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    platforms = serializers.ListField(required=True)
    final_price = serializers.IntegerField(required=True)
    original_price = serializers.IntegerField(required=True)
    offer_ends = serializers.DateTimeField(allow_null=True)
    discount = serializers.IntegerField(allow_null=True)
    image = serializers.CharField(allow_null=True)

    def save(self, product: models.Product):
        title = self.validated_data.get('title')
        platforms = self.validated_data.get('platforms')
        final_price = self.validated_data.get('final_price')
        original_price = self.validated_data.get('original_price')
        offer_ends = self.validated_data.get('offer_ends')
        discount = self.validated_data.get('discount')
        image = self.validated_data.get('image')
        hash = utils.hash_product_publication(
            product.id,
            title,
            [platform for platform in platforms]
        )
        publication = models.ProductPublication.objects.filter(hash=hash)

        if publication:
            publication = publication.first()
            if publication.final_price != final_price:
                async_to_sync(send_admin_notification)({'text': f'Цена на издание товара {publication.product.title} изменилась',
                                                        'level': NotifyLevels.WARN.value})
            publication.final_price = final_price
            publication.original_price = original_price
            publication.discount_deadline = offer_ends
            publication.discount = discount
        else:

            publication = models.ProductPublication(
                product=product,
                title=title,
                final_price=final_price,
                original_price=original_price,
                discount_deadline=offer_ends,
                discount=discount
            )
            publication.set_photo_from_url(image)
            publication.save()
            for platform in platforms:
                publication.platforms.add(models.Platform.objects.get_or_create(name=platform)[0])
            publication.hash = hash
        publication.save()
        return publication


class ChatMessageSerializer(serializers.ModelSerializer):
    order_id = serializers.SlugRelatedField(source='order', slug_field='id', read_only=True)
    manager_id = serializers.SlugRelatedField(source='manager', slug_field='id', read_only=True)
    
    class Meta:
        model = models.ChatMessage
        fields = (
            'created_at',
            'order_id',
            'manager_id',
            'text',
        )


class ProductToParseSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source='id')
    url = serializers.CharField(source='ps_store_url')
    
    class Meta:
        model = models.Product
        fields = (
            'product_id',
            'url',
        )


class PaymentSerializer(serializers.Serializer):
    terminal_key = serializers.CharField()
    amount = serializers.IntegerField()
    order_id = serializers.UUIDField()
    success = serializers.BooleanField()
    status = serializers.CharField()
    payment_id = serializers.CharField()
    error_code = serializers.CharField()
    payment_url = serializers.URLField()
    message = serializers.CharField(allow_null=True)
    details = serializers.CharField(allow_null=True)
