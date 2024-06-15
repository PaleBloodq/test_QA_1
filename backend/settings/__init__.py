
from .celery import app as celery_app
from .settings import (
    TELEGRAM_BOT_URL,
    MEDIA_ROOT,
)

__all__ = [
    'celery_app',
    'TELEGRAM_BOT_URL',
]
