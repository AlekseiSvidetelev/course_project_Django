from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', "email", "full_name", "comment")
    list_filter = ( "email",)
    search_fields = ("email", "full_name", "comment")
