from django.db import models
from django.contrib.auth.models import User
from .base import BaseModel
from .profile import Profile
from ..validators import percent_validator


__all__ = [
    'Order',
    'OrderProduct',
    'PromoCode',
    'ChatMessage',
]


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
