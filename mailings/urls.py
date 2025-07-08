from django.urls import path
from mailings.apps import MailingsConfig

from mailings.views import MailingListView, MailingDetailView, MailingUpdateView, \
    MailingDeleteView, HomeView, MailingCreateView

app_name = MailingsConfig.name

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', MailingListView.as_view(), name='mailings_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
]