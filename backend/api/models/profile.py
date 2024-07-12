import uuid
from typing import Callable
from django.db import models
from .base import BaseModel
from .product import (
    Publication,
    AddOn,
    Subscription,
    AbstractProductPublication,
)


__all__ = [
    'Profile',
    'WishList',
]


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


class WishList(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
        related_name='wishlist')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE,
        null=True, default=None)
    add_on = models.ForeignKey(AddOn, on_delete=models.CASCADE,
        null=True, default=None)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE,
        null=True, default=None)
    
    @classmethod
    def _change(
        cls,
        product_id: uuid.UUID,
        func: Callable[[AbstractProductPublication, str], None]
    ) -> None:
        for model, attr in (
            (Publication, 'publication'),
            (AddOn, 'add_on'),
            (Subscription, 'subscription'),
        ):
            product = model.objects.filter(id=str(product_id)).first()
            if product:
                return func(product, attr)
    
    @classmethod
    def follow(cls, profile: Profile, product_id: uuid.UUID) -> None:
        cls._change(
            product_id,
            lambda product, attr: cls.objects.get_or_create(**{
                'profile': profile,
                attr: product
            })
        )
    
    @classmethod
    def unfollow(cls, profile: Profile, product_id: uuid.UUID) -> None:
        cls._change(
            product_id,
            lambda product, attr: cls.objects.filter(**{
                'profile': profile,
                attr: product
            }).delete()
        )
