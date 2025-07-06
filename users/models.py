from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = None
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите ваш номер телефона",
    )
    tg_name = models.CharField(
        verbose_name="Ник в телеграм", max_length=100, blank=True, null=True
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars",
        blank=True,
        null=True,
        help_text="Загрузите ваш аватар",
    )

    token = models.CharField(
        verbose_name="Токен", max_length=255, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
