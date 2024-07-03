from rest_framework import serializers
from api import models


__all__ = [
    'ProfileSerializer',
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
