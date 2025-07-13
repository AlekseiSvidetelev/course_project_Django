from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from mailings.forms import StyleFormMixin

from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):  #
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class PasswordResetRequestForm(forms.Form):
    """Форма запроса сброса пароля"""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваш email", "autocomplete": "email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            return email
        return email


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
