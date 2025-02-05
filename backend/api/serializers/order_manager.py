from rest_framework import serializers
from api import models


__all__ = [
    'OrderSerializer',
    'ChatMessageSerializer',
    'OrderPreviewSerializer',
]


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        exclude = [
            'id',
            'created_at',
            'updated_at',
            'order',
            'product_id'
        ]


class OrderSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(slug_field='telegram_id', read_only=True)
    status = serializers.SerializerMethodField()
    chat = serializers.SerializerMethodField()
    products = OrderProductSerializer(many=True, source='order_products')
    
    def get_status(self, obj: models.Order) -> str:
        return obj.get_status_display()
    
    def get_chat(self, obj: models.Order) -> list[dict]:
        return ChatMessageSerializer(
            models.ChatMessage.objects.filter(
                order=obj
            ),
            many=True
        ).data
    
    class Meta:
        model = models.Order
        exclude = [
            'created_at',
            'updated_at',
            'promo_code',
            'payment_id',
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    manager = serializers.SlugRelatedField(slug_field='username', read_only=True)
    images = serializers.SerializerMethodField()
    
    def get_order_id(self, obj: models.ChatMessage) -> str:
        return str(obj.order.id)
    
    def get_images(self, obj: models.ChatMessage) -> list[str]:
        images = []
        for image in models.OrderMessageImage.objects.filter(chat_message=obj):
            try:
                images.append(image.image.url)
            except:
                pass
        return images
    
    class Meta:
        model = models.ChatMessage
        fields = (
            'order_id',
            'created_at',
            'manager',
            'text',
            'images',
        )


class OrderPreviewSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    telegram_id = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    def get_last_message(self, obj: models.Order) -> str:
        try:
            return models.ChatMessage.objects.filter(order=obj).latest('created_at').text
        except:
            return 'Заказ создан'
    
    def get_telegram_id(self, obj: models.Order) -> int:
        return obj.profile.telegram_id
    
    def get_status(self, obj: models.Order) -> str:
        return obj.get_status_display()
    
    class Meta:
        model = models.Order
        fields = [
            'id',
            'telegram_id',
            'status',
            'date',
            'last_message',
        ]
