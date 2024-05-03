from django.db.models import signals
from django.dispatch import receiver
from api import models, utils


def ready():
    print('api signals are ready')


@receiver(signals.post_save, sender=models.ProductPublication)
def hash_product_publication(sender, instance: models.ProductPublication, created: bool, **kwargs):
    if created:
        instance.hash = utils.hash_product_publication(
            instance.product.id,
            instance.title,
            [platform.name for platform in instance.platforms.all()]
        )
        instance.save()


@receiver(signals.post_migrate)
def hash_product_publication(sender, **kwargs):
    models.Tag.objects.get_or_create(name='Подписки EA Play', database_name='eaPlay')
    models.Tag.objects.get_or_create(name='Подписки PS Plus', database_name='psPlus')
    models.Tag.objects.get_or_create(name='Офферы', database_name='offers')
    models.Tag.objects.get_or_create(name='Новинки', database_name='new')
    models.Tag.objects.get_or_create(name='Лидеры продаж', database_name='leaders')
