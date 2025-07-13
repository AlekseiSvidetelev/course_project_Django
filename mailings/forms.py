from django import forms
from django.forms import BooleanField

from clients.models import Client
from mailings.models import Mailings
from mailings_message.models import Message


class StyleFormMixin:
    """Класс для задания стилей формам."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (
            field_name,
            field,
        ) in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingsForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailings
        fields = ["message", "clients"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
            self.fields['message'].queryset = Message.objects.filter(owner=user)
