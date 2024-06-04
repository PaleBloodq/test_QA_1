from rest_framework import serializers
from api import models


__all__ = [
    'OrderSerializer',
    'ChatMessageSerializer',
]


class OrderSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(slug_field='telegram_id', read_only=True)
    status = serializers.SerializerMethodField()
    
    def get_status(self, obj: models.Order):
        return obj.get_status_display()
    
    class Meta:
        model = models.Order
        exclude = [
            'created_at',
            'updated_at',
            'promo_code',
            'payment_id',
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = models.ChatMessage
        fields = (
            'created_at',
            'manager',
            'text',
        )
