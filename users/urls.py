from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("logout_confirm/", LoginView.as_view(template_name="logout_confirm.html"), name="logout_confirm"),
    path("logout/", LogoutView.as_view(next_page="catalog:base"), name="logout"),
    # path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
]