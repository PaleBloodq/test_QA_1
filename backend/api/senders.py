from enum import Enum

from channels.layers import get_channel_layer

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
