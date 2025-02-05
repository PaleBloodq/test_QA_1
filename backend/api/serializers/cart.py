from itertools import chain
from rest_framework import serializers
from .. import models
from .catalog import (
    PublicationSerializer,
    AddOnSerializer,
    SubscriptionSerializer
)


__all__ = [
    'CartSerializer',
    'ChangeCartSerializer',
]


class CartSerializer(serializers.ModelSerializer):
    publications = PublicationSerializer(many=True)
    add_ons = AddOnSerializer(many=True)
    subscriptions = SubscriptionSerializer(many=True)
    
    class Meta:
        model = models.Cart
        fields = [
            'publications',
            'add_ons',
            'subscriptions',
        ]

    def to_list(self):
        return list(chain(*self.data.values()))
class ChangeCartSerializer(serializers.Serializer):
    id = serializers.UUIDField()
