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
