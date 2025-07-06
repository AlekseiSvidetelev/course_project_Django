from django.urls import path
from mailings_message.apps import MailingsMessageConfig
from mailings_message.views import MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, \
    MessageDetailView

app_name = MailingsMessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='list_messages'),
    path('detail/<int:pk>/', MessageDetailView.as_view(), name='detail_message'),
    path('create/', MessageCreateView.as_view(), name='create_message'),
    path('update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
]