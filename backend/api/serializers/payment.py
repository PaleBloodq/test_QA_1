from rest_framework import serializers
from api import models


__all__ = [
    'PaymentSerializer',
    'CreatePaymentItemSerializer',
    'CreatePaymentSerializer',
]


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
