import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import User

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
    languages = models.ManyToManyField(Language, verbose_name='Языки')
    release_date = models.DateField('Дата релиза', )
    ps_store_url = models.URLField('Ссылка в PS Store', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='publications')
    platforms = models.ManyToManyField(Platform, verbose_name='Платформы')
    final_price = models.IntegerField('Конечная стоимость')
    original_price = models.IntegerField('Полная стоимость')
    hash = models.CharField('Хэш', max_length=255, null=True, blank=True)
    title = models.CharField('Заголовок', max_length=255, null=True, blank=True)
    duration = models.IntegerField('Длительность в месяцах', null=True, blank=True)
    quantity = models.IntegerField('Количество игровой валюты', null=True, blank=True)
    includes = models.TextField('Включает', null=True, blank=True)
    preview = ProcessedImageField(verbose_name='Превью', format='WEBP', options={'quality': 40}, null=True, blank=True)
    photo = ProcessedImageField(verbose_name='Изображение', format='WEBP', options={'quality': 100}, null=True, blank=True)
    cashback = models.IntegerField('Кэшбек %', default=3, null=True, blank=True, validators=percent_validator)
    ps_plus_discount = models.IntegerField('Скидка PS Plus %', null=True, blank=True, validators=percent_validator)
    discount = models.IntegerField('Скидка %', null=True, blank=True, validators=percent_validator)
    discount_deadline = models.DateField('Окончание скидки', null=True, blank=True)
    
    def clean(self) -> None:
        return super().clean()
    
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
        OK = 'OK', 'Ок'
        PAID = 'PAID', 'Оплачен'
        ERROR = 'ERROR', 'Ошибка'
    
    profile = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='order')
    date = models.DateField('Дата заказа')
    amount = models.IntegerField('Сумма заказа')
    status = models.CharField('Статус', choices=StatusChoices.choices, default=StatusChoices.OK)
    
    def __str__(self) -> str:
        return f'{self.profile} от {self.date}'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_products')
    product = models.CharField('Позиция', max_length=255)
    product_id = models.CharField('ID товара', max_length=255)
    description = models.CharField('Описание', max_length=255)
    price = models.IntegerField('Стоимость')


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
    order = models.ForeignKey(Order, verbose_name='Сообщение', on_delete=models.CASCADE, related_name='chat_message')
    manager = models.ForeignKey(User, verbose_name='Менеджер', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField('Текст сообщения')
    
    class Meta:
        ordering = ['-created_at']
