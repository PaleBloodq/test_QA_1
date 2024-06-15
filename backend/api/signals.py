import json
import os
import requests
from django.db.models import signals
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from api import models, tasks
from api.utils import send_order_to_bot
from api.senders import send_chat_message
from settings import settings


def ready():
    print('api signals are ready')


@receiver(signals.post_migrate)
def hash_product_publication(sender, **kwargs):
    if sender.name != 'api':
        return
    models.Tag.objects.get_or_create(name='Подписки EA Play', database_name='eaPlay')
    models.Tag.objects.get_or_create(name='Подписки PS Plus', database_name='psPlus')
    models.Tag.objects.get_or_create(name='Офферы', database_name='offers')
    models.Tag.objects.get_or_create(name='Новинки', database_name='new')
    models.Tag.objects.get_or_create(name='Лидеры продаж', database_name='leaders')
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*/12',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )
    PeriodicTask.objects.update_or_create(
        name='Update Products',
        defaults={
            'crontab': schedule,
            'task': 'api.tasks.periodic_parse_product_publications_task',
            'args': json.dumps([]),
        },
    )


@receiver(signals.post_delete, sender=models.ProductPublication)
def delete_photo_product_publication(instance: models.ProductPublication, **kwargs):
    to_delete = (instance.product_page_image, instance.offer_image, instance.search_image)
    for file in to_delete:
        try:
            if file.url:
                path = settings.MEDIA_ROOT / file.url.split('/')[-1]
                if path.is_file():
                    path.unlink()
        except:
            continue

@receiver(signals.post_save, sender=models.Order)
def change_order_status(sender, instance: models.Order, created: bool, **kwargs):
    if not created:
        send_order_to_bot(instance)


@receiver(signals.post_save, sender=models.ChatMessage)
def post_save_message(sender, instance: models.ChatMessage, created: bool, **kwargs):
    if created:
        send_chat_message(instance)
        if instance.manager:
            requests.post(
                f'http://{os.environ.get("TELEGRAM_BOT_HOST")}:{os.environ.get("TELEGRAM_BOT_PORT")}/api/order/message/send/',
                json={
                    'user_id': instance.order.profile.telegram_id,
                    'order_id': str(instance.order.id),
                    'text': instance.text
                }
            )

@receiver(signals.post_save, sender=models.Mailing)
def post_save_mailing(sender, instance: models.Mailing, **kwargs):
    if instance.status != models.Mailing.Status.WAITING:
        return
    tasks.send_mailing.apply_async(
        args=[str(instance.id)],
        eta=instance.start_on,
        task_id=f'send_mailing_{instance.id}',
    )
