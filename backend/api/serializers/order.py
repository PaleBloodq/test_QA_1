from rest_framework import serializers
from api import models


__all__ = [
    'OrderProductSerializer',
    'OrderSerializer',
    'ChatMessageSerializer',
]


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
            'email',
            'password',
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
