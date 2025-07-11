from django.db import models

from clients.models import Client
from config import settings
from mailings_message.models import Message


class Mailings(models.Model):
    """ Модель рассылки """

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата старта рассылки', auto_now_add=True)
    end_time = models.DateTimeField(verbose_name='Дата окончания рассылки', blank=True, null=True)
    status = models.CharField(verbose_name='Статус рассылки', max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='Получатели', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец'
    )


    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        if self.status == 'created':
            return f'Создана рассылка {self.message.subject}'
        elif self.status == 'started':
            return f'Запущена рассылка {self.message.subject}'
        else:
            return f'Завершена рассылка {self.message.subject}'


class AttemptSend(models.Model):
    """ Модель попытки отправки """

    attempt_time = models.DateTimeField(verbose_name='Дата и время попытки отправки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус', default=False)
    server_response = models.CharField(verbose_name='Ответ сервера', max_length=255, blank=True, null=True)
    mailing = models.ForeignKey(Mailings, verbose_name='Рассылка', on_delete=models.CASCADE)
    email = models.ForeignKey(Client, verbose_name='Получатель', on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'

    def __str__(self):
        return f'Попытка отправки {self.mailing}'