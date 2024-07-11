import logging
import uuid
from io import BytesIO
import requests
from django.db import models
from django.core.files.base import ContentFile
from imagekit.models import ProcessedImageField
from PIL import Image
from ps_store_api import models as ps_models
from .base import BaseModel
from ..validators import validate_ps_store_url, percent_validator


__all__ = [
    'EnumBaseModel',
    'Platform',
    'Language',
    'Product',
    'Tag',
    'Publication',
    'AddOn',
    'Subscription',
    'AddOnType',
    'AbstractProductPublication',
]


class EnumBaseModel(BaseModel):
    name = models.CharField('Название', max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class Platform(EnumBaseModel):
    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'


class Language(EnumBaseModel):
    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class AddOnType(EnumBaseModel):
    original_name = models.CharField('Название в PS Store', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Тип аддона'
        verbose_name_plural = 'Типы аддонов'


class Product(BaseModel):
    class TypeChoices(models.TextChoices):
        GAME = 'GAME', 'Игра'
        SUBSCRIPTION = 'SUBSCRIPTION', 'Подписка'
        DONATION = 'DONATION', 'Донат'

    title = models.CharField('Заголовок', max_length=255)
    type = models.CharField('Тип', max_length=32, choices=TypeChoices.choices)
    release_date = models.DateField('Дата релиза', null=True, blank=True)
    ps_store_url = models.URLField('Ссылка в PS Store', null=True, blank=True, unique=True)
    parse_release_date = models.BooleanField('Парсить дату релиза', default=True)
    parse_add_ons = models.BooleanField('Парсить аддоны и остальные допы', default=True)
    orders = models.IntegerField('Оплаченных заказов', default=0, editable=False)
    ps_concept = models.OneToOneField(ps_models.Concept, verbose_name='Концепт PS', on_delete=models.SET_NULL, related_name='api_product', null=True, blank=True)
    def clean(self):
        if not self.type in (self.TypeChoices.SUBSCRIPTION, self.TypeChoices.DONATION):
            self.ps_store_url = validate_ps_store_url(self.ps_store_url)
        super().clean()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class AbstractProductPublication(BaseModel):
    typename = 'abstract_product'
    
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss")
    is_main = models.BooleanField(
        'Отображать как основное', default=False)
    platforms = models.ManyToManyField(
        Platform, verbose_name='Платформы', blank=True)
    final_price = models.IntegerField(
        'Конечная стоимость', default=0)
    discount = models.IntegerField(
        'Скидка %', default=0, validators=percent_validator)
    discount_deadline = models.DateField(
        'Окончание скидки', null=True, blank=True)
    ps_plus_final_price = models.IntegerField(
        'Конечная стоимость PS Plus', null=True, blank=True)
    ps_plus_discount = models.IntegerField(
        'Скидка PS Plus %', default=0, validators=percent_validator)
    ps_plus_discount_deadline = models.DateField(
        'Окончание скидки PS Plus', null=True, blank=True)
    languages = models.ManyToManyField(
        Language, verbose_name='Языки', blank=True)
    price_changed = models.BooleanField(
        'Цена изменилась', default=False, editable=False)
    title = models.CharField(
        'Заголовок', max_length=255, null=True)
    includes = models.TextField(
        'Включает', null=True, blank=True)
    product_page_image = ProcessedImageField(
        verbose_name='Изображение (Страница товара)', format='WEBP',
        options={'quality': 60}, null=True, blank=True)
    search_image = ProcessedImageField(
        verbose_name='Изображение (Поиск / главная)', format='WEBP',
        options={'quality': 40}, null=True, blank=True)
    offer_image = ProcessedImageField(
        verbose_name='Изображение (Оффер)', format='WEBP',
        options={'quality': 40}, null=True, blank=True)
    cashback = models.IntegerField(
        'Кэшбек %', default=3, validators=percent_validator)
    parse_image = models.BooleanField(
        'Парсить изображение', default=True)
    parse_ps_plus_price = models.BooleanField(
        'Парсить цену c PS Plus', default=True)
    parse_title = models.BooleanField(
        'Парсить заголовок', default=True)
    parse_price = models.BooleanField(
        'Парсить цену', default=True)
    parse_platforms = models.BooleanField(
        'Парсить платформы', default=True)


    def set_photo_from_url(self, url: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img_io = BytesIO()
                img.save(img_io, format="WEBP", quality=10)
                img_io.seek(0)
                self.product_page_image.save(
                    f"photo_{uuid.uuid4().hex}.webp",
                    ContentFile(img_io.getvalue()), save=False)
                img.save(img_io, format="WEBP", quality=5)
                img_io.seek(0)
                self.search_image.save(f"photo_{uuid.uuid4().hex}.webp",
                    ContentFile(img_io.getvalue()), save=False)
                img_io.seek(0)
                self.offer_image.save(f"photo_{uuid.uuid4().hex}.webp",
                    ContentFile(img_io.getvalue()), save=False)
        except Exception as exc:
            logging.exception(exc)
    
    @property
    def product_type(self) -> str:
        return self.typename
    
    def __str__(self) -> str:
        return f'({self.product.title}) {self.title}'
    
    class Meta:
        abstract = True


class Publication(AbstractProductPublication):
    typename = 'publication'
    
    ps_product = models.OneToOneField(
        ps_models.Product, verbose_name='Товар PS', on_delete=models.DO_NOTHING,
        null=True, blank=True, related_name='api_publication')
    release_date = models.DateField(
        'Дата релиза', null=True, blank=True)
    parse_release_date = models.BooleanField(
        'Парсить дату релиза', default=True)

    class Meta:
        verbose_name = 'Издание'
        verbose_name_plural = 'Издания'


class AddOn(AbstractProductPublication):
    typename = 'add_on'
    
    ps_add_on = models.OneToOneField(ps_models.AddOn, verbose_name='Аддон PS',
        on_delete=models.SET_NULL, null=True, blank=True, related_name='api_add_on')
    type = models.ForeignKey(AddOnType, verbose_name='Тип аддона',
        on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Аддон'
        verbose_name_plural = 'Аддоны'


class Subscription(AbstractProductPublication):
    typename = 'subscription'
    
    duration = models.IntegerField('Длительность в месяцах', null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Tag(EnumBaseModel):
    database_name = models.CharField('Системное название', max_length=255)
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='tags', blank=True)
    publications = models.ManyToManyField(Publication, verbose_name='Издания', related_name='tags', blank=True)
    add_ons = models.ManyToManyField(AddOn, verbose_name='Аддоны', related_name='tags', blank=True)
    subscriptions = models.ManyToManyField(Subscription, verbose_name='Подписки', related_name='tags', blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
