import logging
import uuid
from io import BytesIO

import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField

from api.validators import validate_ps_store_url
from ps_store_api import models as ps_models

percent_validator = MinValueValidator(0), MaxValueValidator(100)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Создан в', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен в', auto_now=True)

    class Meta:
        abstract = True


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


class Product(BaseModel):
    class TypeChoices(models.TextChoices):
        GAME = 'GAME', 'Игра'
        SUBSCRIPTION = 'SUBSCRIPTION', 'Подписка'
        DONATION = 'DONATION', 'Донат'

    title = models.CharField('Заголовок', max_length=255)
    type = models.CharField('Тип', max_length=32, choices=TypeChoices.choices)
    release_date = models.DateField('Дата релиза', null=True, blank=True)
    ps_store_url = models.URLField('Ссылка в PS Store', null=True, blank=True)
    parse_release_date = models.BooleanField('Парсить дату релиза', default=True)
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


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='publications')
    is_main = models.BooleanField('Отображать как основное', default=False)
    platforms = models.ManyToManyField(Platform, verbose_name='Платформы', blank=True)
    final_price = models.IntegerField('Конечная стоимость')
    discount = models.IntegerField('Скидка %', default=0, validators=percent_validator)
    discount_deadline = models.DateField('Окончание скидки', null=True, blank=True)
    ps_plus_final_price = models.IntegerField('Конечная стоимость PS Plus', null=True, blank=True)
    ps_plus_discount = models.IntegerField('Скидка PS Plus %', default=0, validators=percent_validator)
    ps_plus_discount_deadline = models.DateField('Окончание скидки PS Plus', null=True, blank=True)
    languages = models.ManyToManyField(Language, verbose_name='Языки', blank=True)
    price_changed = models.BooleanField('Цена изменилась', default=False, editable=False)
    ps_store_id = models.CharField('PS Store ID', max_length=100, null=True, editable=False)
    title = models.CharField('Заголовок', max_length=255, null=True)
    duration = models.IntegerField('Длительность в месяцах', null=True)
    quantity = models.IntegerField('Количество игровой валюты', null=True)
    includes = models.TextField('Включает', null=True, blank=True)
    product_page_image = ProcessedImageField(verbose_name='Изображение (Страница товара)', format='WEBP', options={'quality': 60}, null=True, blank=True)
    search_image = ProcessedImageField(verbose_name='Изображение (Поиск / главная)', format='WEBP', options={'quality': 40}, null=True, blank=True)
    offer_image = ProcessedImageField(verbose_name='Изображение (Оффер)', format='WEBP', options={'quality': 40}, null=True, blank=True)
    cashback = models.IntegerField('Кэшбек %', default=3, validators=percent_validator)
    parse_image = models.BooleanField('Парсить изображение', default=True)
    parse_ps_plus_price = models.BooleanField('Парсить цену c PS Plus', default=True)
    parse_title = models.BooleanField('Парсить заголовок', default=True)
    parse_price = models.BooleanField('Парсить цену', default=True)
    parse_platforms = models.BooleanField('Парсить платформы', default=True)
    ps_product = models.OneToOneField(ps_models.Product, verbose_name='Товар PS', on_delete=models.SET_NULL, related_name='api_publication', null=True, blank=True)
    ps_add_on = models.OneToOneField(ps_models.AddOn, verbose_name='Аддон PS', on_delete=models.SET_NULL, related_name='api_add_on', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super().save(force_insert, force_update, using, update_fields)

    def set_photo_from_url(self, url: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img_io = BytesIO()
                img.save(img_io, format="WEBP", quality=10)
                img_io.seek(0)
                self.product_page_image.save(f"photo_{uuid.uuid4().hex}.webp", ContentFile(img_io.getvalue()), save=False)
                img.save(img_io, format="WEBP", quality=5)
                img_io.seek(0)
                self.search_image.save(f"photo_{uuid.uuid4().hex}.webp", ContentFile(img_io.getvalue()), save=False)
                img_io.seek(0)
                self.offer_image.save(f"photo_{uuid.uuid4().hex}.webp", ContentFile(img_io.getvalue()), save=False)
        except Exception as e:
            logging.error(e)
    
    def __str__(self) -> str:
        return f'{self.product}: {self.title}'

    class Meta:
        verbose_name = 'Издание'
        verbose_name_plural = 'Издания'


class Tag(EnumBaseModel):
    database_name = models.CharField('Системное название', max_length=255)
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='tags', blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Profile(BaseModel):
    telegram_id = models.BigIntegerField('Телеграм ID', unique=True)
    playstation_email = models.EmailField('E-mail от аккаунта PlayStation', null=True, blank=True)
    playstation_password = models.CharField('Пароль от аккаунта PlayStation', null=True, blank=True)
    bill_email = models.EmailField('E-mail для чеков', null=True, blank=True)
    cashback = models.IntegerField('Баллы', default=0)
    token_seed = models.UUIDField('Семя токена', default=uuid.uuid4)

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        instance = cls.objects.filter(*args, **kwargs)
        if instance:
            return instance.get()
        return None

    def __str__(self) -> str:
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Ожидает оплаты'
        PAID = 'PAID', 'Оплачен'
        ERROR = 'ERROR', 'Ошибка'
        IN_PROGRESS = 'IN_PROGRESS', 'В работе'
        COMPLETED = 'COMPLETED', 'Выполнен'

    profile = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='order')
    date = models.DateField('Дата заказа')
    amount = models.DecimalField('Сумма заказа', max_digits=10, decimal_places=2)
    bill_email = models.EmailField('E-mail для чека')
    spend_cashback = models.BooleanField('Списать баллы')
    spend_cashback_amount = models.IntegerField('Списание кэшбека', default=0)
    status = models.CharField('Статус', choices=StatusChoices.choices, default=StatusChoices.PAYMENT)
    cashback = models.IntegerField('Начисление кэшбека', default=0)
    need_account = models.BooleanField('Нужно создать аккаунт', default=False)
    email = models.EmailField('E-mail', null=True, blank=True)
    password = models.CharField('Пароль', max_length=255, null=True, blank=True)
    promo_code = models.CharField('Промокод', max_length=255, null=True, blank=True)
    promo_code_discount = models.DecimalField('Скидка по промокоду', max_digits=10, decimal_places=2, null=True, blank=True)
    payment_id = models.CharField('ID платежа', null=True, blank=True, editable=False)
    payment_url = models.URLField('Ссылка на оплату', null=True, blank=True, editable=False)
    manager = models.ForeignKey(User, related_name='Менеджер', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f'{self.id} от {self.date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_products')
    product = models.CharField('Позиция', max_length=255)
    product_id = models.UUIDField('ID товара', max_length=255)
    description = models.CharField('Описание', max_length=255)
    final_price = models.DecimalField('Конечная стоимость', max_digits=10, decimal_places=2)


class PromoCode(BaseModel):
    promo_code = models.CharField('Промокод', max_length=255)
    expiration = models.DateTimeField('Дата окончания')
    discount = models.IntegerField('Скидка %', validators=percent_validator)

    def __str__(self) -> str:
        return f'{self.discount}% {self.promo_code}'

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class ChatMessage(BaseModel):
    order = models.ForeignKey(Order, verbose_name='Сообщение', on_delete=models.CASCADE, related_name='chat_messages')
    manager = models.ForeignKey(User, verbose_name='Менеджер', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField('Текст сообщения')

    class Meta:
        ordering = ['created_at']
