from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailings_message.models import Message


def get_mailings_message_from_cache_for_user(user):
    """ Получение списка сообщений из кэша для пользователя"""
    if not CACHE_ENABLED:
        return Message.objects.filter(owner=user)
    key = f"message_{user.id}"
    message = cache.get(key)
    if message is not None:
        return message
    message = Message.objects.filter(owner=user)
    cache.set(key, message, timeout=60*60)
    return message


def get_mailings_message_from_cache_for_superuser():
    """ Получение списка сообщений из кэша для суперпользователя"""
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = 'message'
    message = cache.get(key)
    if message is not None:
        return message
    message = Message.objects.all()
    cache.set(key, message, timeout=60*60)
    return message
