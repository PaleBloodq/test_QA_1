import datetime
import logging
import os
import random

import requests
from asgiref.sync import async_to_sync
from celery_singleton import Singleton

from api import serializers, models
from api.senders import send_admin_notification, NotifyLevels
from settings import celery_app

PRODUCT_PARSER_URL = f'{os.environ.get("PRODUCT_PARSER_SCHEMA")}://{os.environ.get("PRODUCT_PARSER_HOST")}'
if os.environ.get("PRODUCT_PARSER_PORT"):
    PRODUCT_PARSER_URL += f':{os.environ.get("PRODUCT_PARSER_PORT")}'
PRODUCT_PARSER_URL += '/parse'


@celery_app.task(base=Singleton, on_unique=["ignore"])
def parse_product_publications_task(data, need_notify=True):
    logging.warning("Parse product")
    requests.post(
        PRODUCT_PARSER_URL,
        json={
            'data': data,
            'need_notify': need_notify
        }
    )


@celery_app.task(base=Singleton, on_unique=["ignore"])
def periodic_parse_product_publications_task():
    logging.warning("Periodic pars product")
    async_to_sync(send_admin_notification)({'text': 'Начинается парсинг каталога...',
                                                    'level': NotifyLevels.INFO.value})
    #date = datetime.datetime.now() - datetime.timedelta(hours=12)
    #all_products = list(models.Product.objects.filter(updated_at__lt=date.isoformat()).all())
    all_products = list(models.Product.objects.all())
    half_count = (len(all_products) + 1) // 2
    queryset = random.sample(all_products, half_count)
    data = serializers.ProductToParseSerializer(queryset, many=True).data
    parse_product_publications_task.delay(data, False)
