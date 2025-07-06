from django import forms
from .models import Message

class MessageForms(forms.ModelForm):
    """ Класс формы для отправки сообщения """

    class Meta:
        model = Message
        fields = ['subject', 'body']
