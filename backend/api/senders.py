from enum import Enum
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from . import models
from .serializers import order_manager as serializers
from settings import TELEGRAM_BOT_URL


class NotifyLevels(Enum):
    WARN = 'WARN'
    INFO = 'INFO'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'


async def send_admin_notification(message):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "admin_notifications",
        {
            "type": "admin_message",
            "message": message,
        },
    )


async def _send_order_manager(type: str, **kwargs):
    kwargs['type'] = type
    channel_layer = get_channel_layer()
    await channel_layer.group_send('order_manager', kwargs)


def send_chat_message(chat_message: models.ChatMessage):
    if chat_message.manager:
        requests.post(
            f'{TELEGRAM_BOT_URL}/api/order/message/send/',
            json={
                'user_id': chat_message.order.profile.telegram_id,
                'order_id': str(chat_message.order.id),
                'text': chat_message.text
            }
        )
    async_to_sync(_send_order_manager)(
        'chat_message',
        message=serializers.ChatMessageSerializer(chat_message).data
    )


def send_order_created(order: models.Order):
    async_to_sync(_send_order_manager)(
        'new_order',
        order=serializers.OrderSerializer(order).data
    )
