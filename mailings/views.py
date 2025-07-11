
from django.http import HttpResponseRedirect
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
from mailings.models import Mailings, AttemptSend
from mailings.services import send_mailing
from mailings_message.models import Message
from django.contrib import messages


class HomeView(TemplateView):
    """ Главная страница """
    template_name = 'index.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailings.objects.all().count()
        context['active_mailings'] = Mailings.objects.filter(status='started').count()
        context['unique_clients'] = Client.objects.all().count()
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
    ordering = ['-id']
    success_url = reverse_lazy('mailings:mailings_list.html')

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args={self.kwargs.get("pk")})


def start_mailing(request, pk):
    """Запускает рассылку по требованию"""
    mailing = get_object_or_404(Mailings, pk=pk)

    success = send_mailing(pk, request)

    # if success:
    #     mailings = f'Рассылка "{mailing.message.subject}" частично успешно запущена'
    #     status = 'success'
    # else:
    #     mailings = f'Рассылка "{mailing.message.subject}" не запущена'
    #     status = 'error'

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    else:

        return redirect('mailings:mailing_list')

class AttemptListView(ListView):
    """ Список попыток отправки """

    model = AttemptSend
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'
    ordering = ['-attempt_time']
    success_url = reverse_lazy('mailings:mailings_list')

class AttemptDetailView(DetailView):
    """ Просмотр попытки отправки """

    model = AttemptSend
    template_name = 'mailings/attempt_detail.html'
    context_object_name = 'attempt'
    success_url = reverse_lazy('mailings:mailings_list')
