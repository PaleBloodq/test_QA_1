import uuid
import requests
from bs4 import BeautifulSoup
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
    
    def normalize_price(self, price: int):
        if price <= 899:
            exchange_rate = 5.5
        elif 900 <= price <= 1699:
            exchange_rate = 5
        else:
            exchange_rate = 4.5
        price *= exchange_rate
        if price >= 1000 and price % 1000 < 25:
            price -= price % 1000 + 5
        if price % 5 > 0:
            price -= price % 5
        return int(price)
    
    def parse_publications(self):
        if self.ps_store_url:
            for soup_edition in BeautifulSoup(requests.get(self.ps_store_url).text, 'html.parser').find_all('article'):
                try:
                    publication = ProductPublication(
                        product=self,
                        price=self.normalize_price(int(soup_edition.find('span', {'class': 'psw-t-title-m'}).text.split(',')[0].replace('.', ''))),
                        title=soup_edition.find('h3', {'class': 'psw-t-title-s'}).text
                    )
                    for soup_platform in soup_edition.find_all('span', {'class': 'psw-t-tag'}):
                        platform, created = Platform.objects.get_or_create(name=soup_platform.text)
                        publication.platforms.add(platform)
                    publication.save()
                except:
                    pass
    
    def save(self) -> None:
        super().save()
        self.parse_publications()
    
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
    cashback = models.IntegerField('Кэшбек %', null=True, blank=True, validators=percent_validator)
    ps_plus_discount = models.IntegerField('Скидка PS Plus %', null=True, blank=True, validators=percent_validator)
    discount = models.IntegerField('Скидка %', null=True, blank=True, validators=percent_validator)
    discount_deadline = models.DateField('Окончание скидки', null=True, blank=True)
    
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
    telegram_id = models.IntegerField('Телеграм ID', unique=True)
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
    item = models.CharField('Позиция', max_length=255)
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
