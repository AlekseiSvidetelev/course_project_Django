from django.contrib import admin

from mailings.models import Client, Message, MailingList, AttemptSend


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "comment")
    list_filter = ( "email",)
    search_fields = ("email", "full_name", "comment")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject", "body",)

@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "message", )
    list_filter = ("start_time",)



@admin.register(AttemptSend)
class AttemptSendAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "server_response", "message",)
    list_filter = ("attempt_time", )


