from django.db import models
from config import settings


class Message(models.Model):
    """Модель сообщения"""

    subject = models.CharField(verbose_name="Тема", max_length=255)
    body = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ('can_see_all_messages', 'Можно видеть все сообщения'),
        ]

    def __str__(self):
        return self.subject
