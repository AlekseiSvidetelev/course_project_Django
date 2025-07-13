from django.db import models

from config import settings


class Client(models.Model):
    """Модель получатель рассылки"""

    email = models.EmailField(verbose_name="Email", max_length=255)
    full_name = models.CharField(verbose_name="ФИО", max_length=255, blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = (
            ('view_all_clients', "Может просматривать всех получателей"),
        )

    def __str__(self):
        if self.full_name:
            return f"{self.full_name} ({self.email})"
        else:
            return self.email
