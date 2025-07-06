from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView,
)

from message_service.forms import MessageForms
from message_service.models import Message


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MailingListView(ListView):
    """ Список сообщений """

    model = Message
    template_name = 'mailings.html'


class MailingDetailView(DetailView):
    """ Просмотр сообщения """

    model = Message

class MailingCreateView(CreateView):
    """ Создание сообщения """

    model = Message
    form_class = MessageForms
    template_name = 'message_service/message_form.html'
    success_url = '/'

class MailingUpdateView(UpdateView):
    """ Редактирование сообщения """
    pass

class MailingDeleteView(DeleteView):
    """ Удаление сообщения """
    pass


