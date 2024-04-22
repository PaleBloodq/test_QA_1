import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
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
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='publications')
    platforms = models.ManyToManyField(Platform, verbose_name='Платформы')
    price = models.IntegerField('Стоимость')
    title = models.CharField('Заголовок', max_length=255, null=True)
    duration = models.IntegerField('Длительность в месяцах', null=True)
    quantity = models.IntegerField('Количество игровой валюты', null=True)
    includes = models.TextField('Включает', null=True, blank=True)
    preview = models.ImageField('Превью', null=True, blank=True)
    photo = models.ImageField('Изображение', null=True, blank=True)
    cashback = models.IntegerField('Кэшбек %', null=True, blank=True)
    ps_plus_discount = models.IntegerField('Скидка PS Plus %', null=True, blank=True)
    discount = models.IntegerField('Скидка %', null=True, blank=True)
    discount_deadline = models.DateField('Окончание скидки', null=True, blank=True)
    
    def __str__(self) -> str:
        models.RowRange
        return f'{self.product}: {self.title} ({self.platforms})'
    
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
    telegram_id = models.IntegerField('Телеграм ID')
    playstation_email = models.EmailField('E-mail от аккаунта PlayStation', null=True, blank=True)
    playstation_password = models.CharField('Пароль от аккаунта PlayStation', null=True, blank=True)
    bill_email = models.EmailField('E-mail для чеков', null=True, blank=True)
    cashback = models.IntegerField('Баллы', default=0)
    token_seed = models.IntegerField('Семя токена', default=0)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Orders(BaseModel):
    date = models.DateField('Дата заказа')
    amount = models.IntegerField('Сумма заказа')
    

class OrderProduct(BaseModel):
    order = models.ForeignKey(Orders, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_product')
    item = models.CharField('Позиция', max_length=255)
    description = models.CharField('Описание', max_length=255)
    price = models.IntegerField('Стоимость')
