from enum import Enum
from channels.layers import get_channel_layer
from . import models
from .serializers import order_manager as serializers


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


async def send_chat_message(chat_message: models.ChatMessage):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        str(chat_message.order.id),
        {
            'type': 'order_message',
            'data': serializers.ChatMessageSerializer(chat_message).data,
        }
    )


async def send_order_created(order: models.Order):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        'new_order',
        {
            'type': 'order',
            'data': serializers.OrderSerializer(order).data,
        }
    )
