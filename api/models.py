from typing import Collection
import uuid
from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(verbose_name='Создан в', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен в', auto_now=True)
    
    class Meta:
        abstract = True


class EnumBaseModel(BaseModel):
    name = models.CharField(verbose_name='Название', max_length=255, unique=True)
    
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
    
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    type = models.CharField(verbose_name='Тип', max_length=32, choices=TypeChoices.choices)
    language = models.ManyToManyField(Language, verbose_name='Язык')
    release_date = models.DateField(verbose_name='Дата релиза', )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='publications')
    platform = models.ManyToManyField(Platform, verbose_name='Платформа')
    price = models.IntegerField(verbose_name='Стоимость')
    title = models.CharField(verbose_name='Заголовок', max_length=255, null=True)
    duration = models.IntegerField(verbose_name='Длительность в месяцах', null=True)
    quantity = models.IntegerField(verbose_name='Количество игровой валюты', null=True)
    includes = models.TextField(verbose_name='Включает', null=True, blank=True)
    preview = models.ImageField(verbose_name='Превью', null=True, blank=True)
    photo = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    cashback = models.IntegerField(verbose_name='Кэшбек', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.product}: {self.title} ({self.platform})'
    
    class Meta:
        verbose_name = 'Издание'
        verbose_name_plural = 'Издания'


class Tag(EnumBaseModel):
    database_name = models.CharField(verbose_name='Системное название', max_length=255)
    product = models.ManyToManyField(Product, verbose_name='Товар', related_name='tag', blank=True)
        
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
