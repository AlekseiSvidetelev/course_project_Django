from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from clients.forms import ClientForm
from clients.models import Client


class ClientsListView(ListView):
    """ Представление для списка клиентов """

    model = Client
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients'


class ClientsDetailView(DetailView):
    """ Представление для детальной информации о клиенте """

    model = Client
    template_name = 'clients/clients_detail.html'


class ClientsCreateView(CreateView):
    """ Представление для создания клиента """

    model = Client
    form_class = ClientForm
    template_name = 'clients/clients_form.html'
    success_url = reverse_lazy('clients:clients_list')


class ClientsUpdateView(UpdateView):
    """ Представление для редактирования клиента """

    model = Client
    form_class = ClientForm
    template_name = 'clients/clients_form.html'
    success_url = reverse_lazy('clients:clients_list')

    def get_success_url(self):
        return reverse("clients:clients_detail", args={self.kwargs.get("pk")})


class ClientsDeleteView(DeleteView):
    """ Представление для удаления клиента """

    model = Client
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('clients:clients_list')
