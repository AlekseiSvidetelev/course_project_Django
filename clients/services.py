from django.core.cache import cache

from clients.models import Client
from config.settings import CACHE_ENABLED


def get_clients_from_cache_for_user(user):
    """ Получение списка клиентов из кэша для пользователя"""
    if not CACHE_ENABLED:
        return Client.objects.filter(owner=user)
    key = f"clients_{user.id}"
    clients = cache.get(key)
    if clients is not None:
        return clients
    clients = Client.objects.filter(owner=user)
    cache.set(key, clients, timeout=60*60)
    return clients


def get_client_from_cache_for_superuser():
    """ Получение списка клиентов из кэша для суперпользователя"""
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = 'clients'
    clients = cache.get(key)
    if clients is not None:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients, timeout=60*60)
    return clients
