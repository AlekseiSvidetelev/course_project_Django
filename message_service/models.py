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


class Message(models.Model):
    """ Модель сообщения """

    subject = models.CharField(verbose_name='Тема', max_length=255)
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class MailingList(models.Model):
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

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]
    attempt_time = models.DateTimeField(verbose_name='Дата и время попытки отправки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='success')
    server_response = models.CharField(verbose_name='Ответ сервера', max_length=255, blank=True, null=True)
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'

    def __str__(self):
        if self.status == 'success':
            return f'Успешно отправлено {self.message.subject}'
        else:
            return f'Не успешно отправлено {self.message.subject}'