from rest_framework import serializers
from api import models
from .catalog import (
    PublicationWithProductSerializer,
    AddOnWithProductSerializer,
    SubscriptionWithProductSerializer,
)


__all__ = [
    'ProfileSerializer',
    'wishlist_serializer',
    'ChangeWishListSerializer',
]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = (
            'playstation_email',
            'playstation_password',
            'bill_email',
            'cashback',
        )


def wishlist_serializer(profile: models.Profile):
    wishlist = []
    for item in models.WishList.objects.filter(profile=profile):
        if item.publication:
            wishlist.append(
                PublicationWithProductSerializer(item.publication).data)
        if item.add_on:
            wishlist.append(AddOnWithProductSerializer(item.add_on).data)
        if item.subscription:
            wishlist.append(
                SubscriptionWithProductSerializer(item.subscription).data)
    return wishlist


class ChangeWishListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
