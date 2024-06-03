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
    item = serializers.CharField(source='product')
    
    class Meta:
        model = models.OrderProduct
        fields = (
            'item',
            'description',
            'final_price',
        )


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='profile.telegram_id')
    order_id = serializers.UUIDField(source='id')
    order_products = OrderProductSerializer(many=True)
    
    class Meta:
        model = models.Order
        fields = (
            'user_id',
            'order_id',
            'date',
            'amount',
            'order_products',
            'payment_url',
            'need_account',
            'status',
        )


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


class CreatePaymentItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product')
    price = serializers.DecimalField(source='final_price', max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(default=1)
    amount = serializers.DecimalField(source='final_price', max_digits=10, decimal_places=2)
    
    class Meta:
        model = models.OrderProduct
        fields = [
            'name',
            'price',
            'quantity',
            'amount',
        ]


class CreatePaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source='id')
    description = serializers.CharField(source='__str__')
    customer_telegram_id = serializers.IntegerField(source='profile.telegram_id')
    items = CreatePaymentItemSerializer(source='order_products', many=True)
    
    class Meta:
        model = models.Order
        fields = [
            'order_id',
            'amount',
            'description',
            'customer_telegram_id',
            'bill_email',
            'items',
        ]
