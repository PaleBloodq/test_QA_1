import uuid
from django.db import models


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


class Type(EnumBaseModel):
    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'


class Platform(EnumBaseModel):
    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'


class Language(EnumBaseModel):
    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

class Donation(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    preview = models.ImageField(verbose_name='Превью', null=True, blank=True)
    photo = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    release_date = models.DateField(verbose_name='Дата релиза', )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'


class DonationQuantity(BaseModel):
    donation = models.ForeignKey(Donation, verbose_name='Донат', on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, verbose_name='Платформа', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', )
    price = models.IntegerField(verbose_name='Стоимость', )
    
    def __str__(self) -> str:
        return f'{self.donation}: {self.quantity} ({self.platform})'


class Product(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    type = models.ForeignKey(Type, verbose_name='Тип', on_delete=models.CASCADE)
    release_date = models.DateField(verbose_name='Дата релиза', )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='publications')
    platform = models.ForeignKey(Platform, verbose_name='Платформа', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    price = models.IntegerField(verbose_name='Стоимость', )
    includes = models.TextField(verbose_name='Включает', )
    preview = models.ImageField(verbose_name='Превью', null=True, blank=True)
    photo = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    cashback = models.IntegerField(verbose_name='Кэшбек', null=True, blank=True)
    duration = models.IntegerField(verbose_name='Длительность', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.product}: {self.title} ({self.platform})'


class Tag(EnumBaseModel):
    database_name = models.CharField(verbose_name='Системное название', max_length=255)
        
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ProductTag(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='tag')
    tag = models.ForeignKey(Tag, verbose_name='Тег', on_delete=models.CASCADE)
