from django.contrib import admin

from mailings.models import Client, Message, MailingList, AttemptSend


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "message", )
    list_filter = ("start_time",)
