import logging
import random
from time import sleep
from asgiref.sync import async_to_sync
from celery_singleton import Singleton
from api import models, utils
from api.senders import send_admin_notification, NotifyLevels
from settings import celery_app
from services.ps_store_api import PS_StoreAPI


@celery_app.task(base=Singleton, on_unique=["ignore"])
def parse_product_publications_task(product_ids: list[str], need_notify=True):
    api = PS_StoreAPI()
    products = models.Product.objects.filter(id__in=product_ids, type=models.Product.TypeChoices.GAME)
    for product in products:
        logging.warning(f'Parse product {product.title}')
        if product.ps_store_url is None:
            logging.warning('No url found.')
            continue
        editions = api.get_by_url(product.ps_store_url)
        logging.warning(f'{len(editions)} editions found.')
        for edition in editions:
            try:
                if product.parse_release_date and product.release_date != edition.release_date:
                    product.release_date = edition.release_date
                    product.save()
                publication = models.ProductPublication.objects.filter(ps_store_id=edition.id).first()
                if publication is None:
                    publication = models.ProductPublication(
                        product=product,
                        ps_store_id=edition.id,
                    )
                if publication.parse_title:
                    publication.title = edition.name
                if publication.parse_price:
                    if publication.final_price != edition.price.discounted_price:
                        publication.price_changed = True
                        async_to_sync(send_admin_notification)({
                            'text': f'Цена на издание товара {publication.product.title} изменилась',
                            'level': NotifyLevels.WARN.value,
                        })
                    publication.final_price = utils.normalize_price(edition.price.discounted_price, True)
                    publication.discount = edition.price.discount
                    publication.discount_deadline = edition.price.discount_deadline
                if publication.parse_ps_plus_price:
                    publication.ps_plus_final_price = utils.normalize_price(edition.ps_plus_price.discounted_price, True)
                    publication.ps_plus_discount = edition.ps_plus_price.discount
                    publication.ps_plus_discount_deadline = edition.ps_plus_price.discount_deadline
                if publication.parse_image:
                    if not all((publication.product_page_image, publication.search_image, publication.offer_image)):
                        publication.set_photo_from_url(edition.image)
                publication.save()
                if publication.parse_platforms:
                    for platform in edition.platforms:
                        platform = models.Platform.objects.get_or_create(name=platform)[0]
                        publication.platforms.add(platform)
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
    #date = datetime.datetime.now() - datetime.timedelta(hours=12)
    #all_products = list(models.Product.objects.filter(updated_at__lt=date.isoformat()).all())
    all_products = list(models.Product.objects.all())
    half_count = (len(all_products) + 1) // 2
    queryset = random.sample(all_products, half_count)
    parse_product_publications_task.delay([str(product.id) for product in queryset], False)
