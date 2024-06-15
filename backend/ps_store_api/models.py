from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Concept(models.Model):
    id = models.IntegerField('ID', primary_key=True, unique=True)
    name = models.CharField('Название', max_length=128, null=True, blank=True)
    release_date = models.DateTimeField('Дата релиза', null=True, blank=True)
    publisher_name = models.CharField('Издатель', max_length=128, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'


class Platform(models.Model):
    name = models.CharField('Название', max_length=32)
    
    def __str__(self) -> str:
        return f'{self.name}'


class Mobilecta(models.Model):
    type = models.CharField('Тип', max_length=64)
    base_price = models.DecimalField('Цена без скидки', max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2)
    discount = models.IntegerField('Скидка %', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    discount_deadline = models.DateTimeField('Окончание скидки', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.base_price} / {self.discounted_price} ({self.discount}%)'


class AbstractProduct(models.Model):
    id = models.CharField('ID', primary_key=True, unique=True, max_length=128)
    concept = models.ForeignKey(Concept, verbose_name='Концепт', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=128)
    platforms = models.ManyToManyField(Platform, verbose_name='Платформы', blank=True)
    price = models.OneToOneField(Mobilecta, verbose_name='Цена', on_delete=models.CASCADE, related_name='+')
    ps_plus_price = models.OneToOneField(Mobilecta, verbose_name='Цена PS Plus', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    portrait_image = models.URLField('Изображение', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        abstract = True


class Product(AbstractProduct):
    np_title_id = models.CharField('npTitleId', max_length=32)
    release_date = models.DateTimeField('Дата релиза')


class AddOn(AbstractProduct):
    pass
