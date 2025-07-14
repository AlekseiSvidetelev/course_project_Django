from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from mailings_message.models import Message
from mailings_message.forms import MessageForms
from mailings_message.services import get_mailings_message_from_cache_for_superuser, \
    get_mailings_message_from_cache_for_user


class MessageListView(LoginRequiredMixin, ListView):
    """Список сообщений"""

    model = Message
    template_name = "mailings_message/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.has_perm("mailings_message.can_see_all_messages"):
            return get_mailings_message_from_cache_for_superuser()
        else:
            return get_mailings_message_from_cache_for_user(user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""

    model = Message
    form_class = MessageForms
    template_name = "mailings_message/message_form.html"
    success_url = reverse_lazy("mailings_message:list_messages")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр сообщения"""

    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения"""

    model = Message
    form_class = MessageForms
    template_name = "mailings_message/message_form.html"
    success_url = reverse_lazy("mailings_message:list_messages")

    def get_success_url(self):
        return reverse("mailings_message:detail_message", args={self.kwargs.get("pk")})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""

    model = Message
    template_name = "mailings_message/message_delete.html"
    success_url = reverse_lazy("mailings_message:list_messages")
