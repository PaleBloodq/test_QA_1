
from .celery import app as celery_app
from .settings import TELEGRAM_BOT_URL

__all__ = [
    'celery_app',
    'TELEGRAM_BOT_URL',
]
