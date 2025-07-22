from django.contrib import admin

from mailings_message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "body",
        "owner",
    )
    list_filter = ("subject",)
    search_fields = (
        "subject",
        "body",
    )
