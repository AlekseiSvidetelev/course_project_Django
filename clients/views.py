from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from clients.forms import ClientForm
from clients.models import Client
from clients.services import get_clients_from_cache_for_user, get_client_from_cache_for_superuser


class ClientsListView(LoginRequiredMixin, ListView):
    """Представление для списка клиентов"""

    model = Client
    template_name = "clients/clients_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.has_perm("clients.view_all_clients"):
            return get_client_from_cache_for_superuser()
        else:
            return get_clients_from_cache_for_user(user)


class ClientsDetailView(LoginRequiredMixin, DetailView):
    """Представление для детальной информации о клиенте"""

    model = Client
    template_name = "clients/clients_detail.html"


class ClientsCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания клиента"""

    model = Client
    form_class = ClientForm
    template_name = "clients/clients_form.html"
    success_url = reverse_lazy("clients:clients_list")

    def form_valid(self, form):
        client = form.save(commit=False)
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientsUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования клиента"""

    model = Client
    form_class = ClientForm
    template_name = "clients/clients_form.html"
    success_url = reverse_lazy("clients:clients_list")

    def get_success_url(self):
        return reverse("clients:clients_detail", args={self.kwargs.get("pk")})


class ClientsDeleteView(DeleteView):
    """Представление для удаления клиента"""

    model = Client
    template_name = "clients/clients_confirm_delete.html"
    success_url = reverse_lazy("clients:clients_list")
