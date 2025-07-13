from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView, RedirectView,
)

from clients.models import Client
from mailings.forms import MailingsForms
from mailings.models import Mailings, AttemptSend
from mailings.services import send_mailing
from mailings_message.models import Message


class HomeView(TemplateView):
    """Главная страница"""

    template_name = "mailings/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context["total_mailings"] = Mailings.objects.filter(owner=user).count()
            context["active_mailings"] = Mailings.objects.filter(owner=user, status="started").count()
            context["unique_clients"] = Client.objects.filter(mailings__owner=user).distinct().count()
            successful_attempts = AttemptSend.objects.filter(mailing__owner=user, status=True).count()
            failed_attempts = AttemptSend.objects.filter(mailing__owner=user, status=False).count()
            total_attempts = successful_attempts + failed_attempts
            context["successful_attempts"] = successful_attempts
            context["failed_attempts"] = failed_attempts
            context["total_attempts"] = total_attempts

        return context


class MailingListView(LoginRequiredMixin, ListView):
    """Список рассылок"""

    model = Mailings
    template_name = "mailings/mailings_list.html"
    context_object_name = "mailings"
    ordering = ["-start_time"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser  or user.has_perm("mailings.can_stoped"):
            return Mailings.objects.all()
        else:
            return Mailings.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.all()
        context["recipients"] = Client.objects.all()
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создать рассылку"""

    model = Mailings
    form_class = MailingsForms
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр сообщения"""

    model = Mailings
    template_name = "mailings/mailing_detail.html"
    context_object_name = "object"


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения"""

    model = Mailings
    form_class = MailingsForms
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.all()
        context["recipients"] = Client.objects.all()
        return context

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args={self.kwargs.get("pk")})


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""

    model = Mailings
    template_name = "mailings/mailing_confirm_delete.html"
    ordering = ["-id"]
    success_url = reverse_lazy("mailings:mailings_list.html")

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args={self.kwargs.get("pk")})


def start_mailing(request, pk):
    """Запускает рассылку по требованию"""
    mailing = get_object_or_404(Mailings, pk=pk)
    success = send_mailing(pk, request)
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect("mailings:mailing_list")


class AttemptListView(LoginRequiredMixin, ListView):
    """Список попыток отправки"""

    model = AttemptSend
    template_name = "mailings/attempt_list.html"
    context_object_name = "attempts"
    ordering = ["-attempt_time"]
    success_url = reverse_lazy("mailings:mailings_list")

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AttemptSend.objects.all()
        else:
            return AttemptSend.objects.filter(mailing__owner=user)


class AttemptDetailView(LoginRequiredMixin, DetailView):
    """Просмотр попытки отправки"""

    model = AttemptSend
    template_name = "mailings/attempt_detail.html"
    context_object_name = "attempt"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AttemptSend.objects.all()
        else:
            return AttemptSend.objects.filter(mailing__owner=self.request.user)


class MailingStopView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    """Представление для остановки рассылки"""

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('mailings.can_stoped')

    def get_redirect_url(self, *args, **kwargs):
        mailing = Mailings.objects.get(pk=kwargs['pk'])
        mailing.status = 'finished'
        mailing.save()
        return reverse_lazy('mailings:mailing_detail', args=(mailing.pk,))
