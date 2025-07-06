from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from mailings_message.models import Message
from mailings_message.forms import MessageForms

class MessageListView(ListView):
    """ Список сообщений """
    model = Message
    template_name = 'mailings_message/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    """ Создание сообщения """

    model = Message
    form_class = MessageForms
    template_name = 'mailings_message/message_form.html'
    success_url = reverse_lazy('mailings_message:list_messages')


class MessageDetailView(DetailView):
    """ Просмотр сообщения """

    model = Message


class MessageUpdateView(UpdateView):
    """ Редактирование сообщения """

    model = Message
    form_class = MessageForms
    template_name = 'mailings_message/message_form.html'
    success_url = reverse_lazy('mailings_message:list_messages')

    def get_success_url(self):
        return reverse("mailings_message:detail_message", args={self.kwargs.get("pk")})


class MessageDeleteView(DeleteView):
    """ Удаление сообщения """

    model = Message
    template_name = 'mailings_message/message_delete.html'
    success_url = reverse_lazy('mailings_message:list_messages')
