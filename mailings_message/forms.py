from django import forms

from mailings.forms import StyleFormMixin
from mailings_message.models import Message

class MessageForms(StyleFormMixin, forms.ModelForm):
    """ Класс формы для отправки сообщения """

    class Meta:
        model = Message
        fields = ['subject', 'body']
