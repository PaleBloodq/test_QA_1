from django.db import models
from .profile import Profile
from .base import BaseModel
from .product import Publication, AddOn, Subscription


__all__ = [
    'Cart',
]


class Cart(BaseModel):
    profile = models.OneToOneField(Profile, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='cart')
    publications = models.ManyToManyField(Publication, verbose_name='Издания', blank=True)
    add_ons = models.ManyToManyField(AddOn, verbose_name='Издания', blank=True)
    subscriptions = models.ManyToManyField(Subscription, verbose_name='Издания', blank=True)
