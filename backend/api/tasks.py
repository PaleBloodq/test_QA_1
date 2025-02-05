import logging
import random
from time import sleep
import requests
from asgiref.sync import async_to_sync
from celery_singleton import Singleton
from api import models, utils, serializers
from api.senders import send_admin_notification, NotifyLevels
from settings import celery_app, TELEGRAM_BOT_URL
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
                utils.update_publication(models.Publication.objects.get_or_create(
                    dict(
                        product=product
                    ),
                    ps_product=ps_product,
                )[0])
            except Exception as exc:
                logging.exception(exc)
        if product.parse_add_ons:
            for ps_add_on in ps_models.AddOn.objects.filter(concept=ps_concept):
                try:
                    utils.update_publication(models.AddOn.objects.get_or_create(
                        dict(
                            product=product,
                            type=models.AddOnType.objects.get_or_create(
                                dict(
                                    name=ps_add_on.type.name
                                ),
                                original_name=ps_add_on.type.name
                            )[0]
                        ),
                        ps_add_on=ps_add_on,
                    )[0])
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


@celery_app.task(bind=True)
def send_mailing(task, mailing_id: str):
    mailing = models.Mailing.objects.filter(id=mailing_id).first()
    if mailing is None:
        return
    try:
        data = serializers.SendMailingSerializer(mailing).data
        mailing.sent_count = len(data['telegram_ids'])
        logging.info(f'Sending mailing tg_bot.')
        response = requests.post(
            TELEGRAM_BOT_URL+'/api/mailing/',
            json=data,
        )
        status_code = response.status_code
    except Exception as exc:
        logging.exception(exc)
        status_code = -1
    finally:
        if status_code == 201:
            mailing.status = models.Mailing.Status.MAILING
        else:
            mailing.status = models.Mailing.Status.ERROR
        mailing.save()


@celery_app.task(bind=True)
def check_order_expired(task, order_id: str):
    order = models.Order.objects.filter(id=order_id).first()
    if order is None:
        return
    if order.status != models.Order.StatusChoices.PAYMENT:
        return
    order.profile.cashback += order.spend_cashback_amount
    order.profile.save()
    utils.restore_cart(order)
    order.delete()
