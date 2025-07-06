from django.urls import path
from message_service.apps import MessageServiceConfig

from message_service.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, HomeView

app_name = MessageServiceConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'), #
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/edit/<int:pk>/', MailingCreateView.as_view(), name='edit_mailing'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
]