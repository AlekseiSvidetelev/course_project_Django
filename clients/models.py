from django.db import models


class Client(models.Model):
    """ Модель получатель рассылки """

    email = models.EmailField(verbose_name='Email', unique=True, max_length=255)
    full_name = models.CharField(verbose_name='ФИО', max_length=255, blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)


    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        if self.full_name:
            return f'{self.full_name} ({self.email})'
        else:
            return self.email