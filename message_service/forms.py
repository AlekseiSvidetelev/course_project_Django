from message_service.models import Message


class MessageForms:
    """ Формы для сообщений """

    class Meta:
        model = Message
        fields = ['_all__']

