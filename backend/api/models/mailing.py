from django.db import models
from django.utils import timezone
from .base import BaseModel


__all__ = [
    'Mailing',
    'MailingMedia',
]


class Mailing(BaseModel):
    class Status(models.TextChoices):
        WAITING = 'WAITING', 'Ожидание рассылки'
        MAILING = 'MAILING', 'Рассылка'
        COMPLETED = 'COMPLETED', 'Выполнено'
        ERROR = 'ERROR', 'Ошибка'
    
    text = models.TextField('Текст рассылки')
    start_on = models.DateTimeField('Начало рассылки', default=timezone.now)
    status = models.CharField('Статус', choices=Status.choices, default=Status.WAITING)
    sent_count = models.IntegerField('Количество получателей', default=0, editable=False)
    received_count = models.IntegerField('Количество получивших', default=0, editable=False)
    messages_ids = models.JSONField('ID отправленных сообщений', default=dict, editable=False)
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingMedia(BaseModel):
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE)
    media = models.FileField('Медиа')
