import logging
import random
from asgiref.sync import async_to_sync
from celery_singleton import Singleton
from api import models, utils
from api.senders import send_admin_notification, NotifyLevels
from settings import celery_app
from services.ps_store_api import PS_StoreAPI


@celery_app.task(base=Singleton, on_unique=["ignore"])
def parse_product_publications_task(product_ids: list[str], need_notify=True):
    logging.warning("Parse product")
    api = PS_StoreAPI()
    products = models.Product.objects.filter(id__in=product_ids)
    for product in products:
        for edition in api.get_by_url(product.ps_store_url):
            publication = models.ProductPublication.objects.filter(ps_store_id=edition.id).first()
            if publication:
                if not publication.parsing_enabled:
                    async_to_sync(send_admin_notification)({
                        'text': f'Цена на издание товара {publication.product.title} изменилась',
                        'level': NotifyLevels.WARN.value,
                    })
                    publication.price_changed = False
                    publication.save()
                    return publication
                if publication.final_price != edition.price.discounted_price:
                    publication.price_changed = True
                publication.final_price = utils.normalize_price(edition.price.discounted_price, True)
                publication.original_price = utils.normalize_price(edition.price.base_price, True)
                publication.discount_deadline = edition.price.discount
                publication.discount_deadline = edition.price.discount_deadline
            else:
                publication = models.ProductPublication(
                    product=product,
                    title=edition.name,
                    ps_store_id=edition.id,
                    final_price=utils.normalize_price(edition.price.discounted_price, True),
                    original_price=utils.normalize_price(edition.price.base_price, True),
                    discount=edition.price.discount,
                    discount_deadline=edition.price.discount_deadline,
                )
            publication.save()
            for platform in edition.platforms:
                publication.platforms.add(models.Platform.objects.get_or_create(name=platform)[0])
            logging.warning(publication)
    async_to_sync(send_admin_notification)({
        'text': f'Парсинг завершился',
        'level': NotifyLevels.WARN.value,
    })


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
    parse_product_publications_task.delay([str(product.id) for product in queryset], False)
