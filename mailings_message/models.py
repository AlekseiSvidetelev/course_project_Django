from django.db import models


class Message(models.Model):
    """ Модель сообщения """

    subject = models.CharField(verbose_name='Тема', max_length=255)
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject
