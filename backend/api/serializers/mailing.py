from rest_framework import serializers
from .. import models


__all__ = [
    'SendMailingSerializer',
    'UpdateMailingSerializer',
]


class MailingButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MailingButton
        fields = [
            'text',
            'url'
        ]


class SendMailingSerializer(serializers.ModelSerializer):
    telegram_ids = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    buttons = serializers.SerializerMethodField()
    
    def get_telegram_ids(self, obj: models.Mailing) -> list[int]:
        return list(models.Profile.objects.all().values_list(
            'telegram_id', flat=True
        ))
    
    def get_media(self, obj: models.Mailing) -> list[str]:
        return [
            media.media.url
            for media in models.MailingMedia.objects.filter(mailing=obj)
        ]
    
    def get_buttons(self, obj: models.Mailing) -> list[dict]:
        return MailingButtonSerializer(
            models.MailingButton.objects.filter(mailing=obj),
            many=True
        ).data
    
    class Meta:
        model = models.Mailing
        fields = [
            'id',
            'telegram_ids',
            'text',
            'media',
            'buttons',
        ]


class UpdateMailingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    status = serializers.ChoiceField(choices=models.Mailing.Status.choices, required=True)
    received_count = serializers.IntegerField(required=True)
    messages_ids = serializers.JSONField(required=True)
    
    class Meta:
        model = models.Mailing
        fields = [
            'id',
            'status',
            'received_count',
            'messages_ids',
        ]
