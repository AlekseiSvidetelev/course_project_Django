from django.urls import path
from clients.apps import ClientsConfig
from clients.views import ClientsCreateView, ClientsListView, ClientsUpdateView, ClientsDeleteView, ClientsDetailView

app_name = ClientsConfig.name

urlpatterns = [
    path("", ClientsListView.as_view(), name="clients_list"),
    path("detail/<int:pk>/", ClientsDetailView.as_view(), name="clients_detail"),
    path("create/", ClientsCreateView.as_view(), name="clients_create"),
    path("update/<int:pk>/", ClientsUpdateView.as_view(), name="clients_update"),
    path("delete/<int:pk>/", ClientsDeleteView.as_view(), name="clients_delete"),
]
