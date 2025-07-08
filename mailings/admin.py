from django.contrib import admin

from mailings.models import Mailings, AttemptSend


@admin.register(Mailings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('show_clients', 'message', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'start_time')
    filter_horizontal = ('clients', )

    def show_clients(self, obj):
        return ', '.join(str(client) for client in obj.clients.all())
    show_clients.short_description = 'Получатели'


@admin.register(AttemptSend)
class AttemptSendAdmin(admin.ModelAdmin):
    list_display = ('message', 'status', 'attempt_time', 'server_response')
    list_filter = ('status', 'attempt_time')