import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class EnumBaseModel(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    
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
    title = models.CharField(max_length=255)
    preview = models.ImageField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    release_date = models.DateField()
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'


class DonationQuantity(BaseModel):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()


class Product(BaseModel):
    title = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    release_date = models.DateField()
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductPublication(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='publications')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    preview = models.ImageField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    includes = models.TextField()
    cashback = models.IntegerField(null=True, blank=True)


class ProductDuration(BaseModel):
    product_publication = models.ForeignKey(ProductPublication, on_delete=models.CASCADE)
    duration = models.IntegerField()


class Tag(EnumBaseModel):
    database_name = models.CharField(max_length=255)
        
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ProductTag(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tag')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
