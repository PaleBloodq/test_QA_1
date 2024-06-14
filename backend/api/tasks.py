import logging
import random
from time import sleep
from asgiref.sync import async_to_sync
from celery_singleton import Singleton
from api import models, utils
from api.senders import send_admin_notification, NotifyLevels
from settings import celery_app
from ps_store_api.api import PS_StoreAPI
from ps_store_api import models as ps_models


@celery_app.task(base=Singleton, on_unique=["ignore"])
def parse_product_publications_task(product_ids: list[str], need_notify=True):
    api = PS_StoreAPI()
    products = models.Product.objects.filter(id__in=product_ids, type=models.Product.TypeChoices.GAME)
    for product in products:
        logging.warning(f'Parse product {product.title}')
        if product.ps_store_url is None:
            logging.warning('No url found.')
            continue
        ps_concept = api.parse_by_url(product.ps_store_url)
        if ps_concept is None:
            logging.warning('No concept found.')
            continue
        product = utils.update_product(product, ps_concept)
        for ps_product in ps_models.Product.objects.filter(concept=ps_concept):
            try:
                utils.update_product_publication(product, ps_product)
            except Exception as exc:
                logging.exception(exc)
        for ps_add_on in ps_models.AddOn.objects.filter(concept=ps_concept):
            try:
                utils.update_product_publication(product, ps_add_on)
            except Exception as exc:
                logging.exception(exc)
        sleep(random.randint(3, 5))
    async_to_sync(send_admin_notification)({
        'text': f'Парсинг завершился',
        'level': NotifyLevels.WARN.value,
    })


@celery_app.task(base=Singleton, on_unique=["ignore"])
def periodic_parse_product_publications_task():
    logging.warning("Periodic pars product")
    async_to_sync(send_admin_notification)({'text': 'Начинается парсинг каталога...',
                                                    'level': NotifyLevels.INFO.value})
    queryset = list(models.Product.objects.all())
    parse_product_publications_task.delay([str(product.id) for product in queryset], False)
