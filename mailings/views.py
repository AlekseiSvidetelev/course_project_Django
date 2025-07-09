from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView,
)

from clients.models import Client
from mailings.forms import MailingsForms
from mailings.models import Mailings
from mailings.services import send_message
from mailings_message.models import Message
from django.contrib import messages


class HomeView(TemplateView):
    """ Главная страница """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MailingListView(ListView):
    """ Список рассылок """

    model = Mailings
    template_name = 'mailings/mailings_list.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.all()
        context['recipients'] = Client.objects.all()
        return context


class MailingCreateView(CreateView):
    """ Создать рассылку """

    model = Mailings
    form_class = MailingsForms
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')


class MailingDetailView(DetailView):
    """ Просмотр сообщения """

    model = Mailings
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'object'


class MailingUpdateView(UpdateView):
    """ Редактирование сообщения """

    model = Mailings
    form_class = MailingsForms
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.all()
        context['recipients'] = Client.objects.all()
        return context

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args={self.kwargs.get("pk")})


class MailingDeleteView(DeleteView):
    """ Удаление сообщения """

    model = Mailings
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailings_list.html')

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args={self.kwargs.get("pk")})


def start_mailing(request, pk):
    """Запускает рассылку по требованию"""
    mailing = get_object_or_404(Mailings, pk=pk)

    if send_message(pk, request):
        messages.success(request, f"Рассылка '{mailing.message.subject}' успешно запущена!")
    else:
        messages.error(request, f"При запуске рассылки '{mailing.message.subject}' произошли ошибки")

    return redirect('mailings:detail_mailing', pk=pk)

