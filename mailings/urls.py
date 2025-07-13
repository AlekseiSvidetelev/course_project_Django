from django.urls import path
from mailings.apps import MailingsConfig

from mailings.views import (
    MailingListView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
    HomeView,
    MailingCreateView,
    start_mailing,
    AttemptListView,
    AttemptDetailView,
    MailingStopView,
)

app_name = MailingsConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("", MailingListView.as_view(), name="mailings_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("start/<int:pk>/", start_mailing, name="start_mailing"),
    path("attempts/", AttemptListView.as_view(), name="attempt_list"),
    path("attempts/<int:pk>/", AttemptDetailView.as_view(), name="attempt_detail"),
    path("stop/<int:pk>/", MailingStopView.as_view(), name="mailing_stop"),
]
