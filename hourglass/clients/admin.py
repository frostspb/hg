from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ["id", "name", "client_type", "client_since", "active", "created"]
    search_fields = ["name", "id"]
    fields = ["name", "client_type", "total_campaigns", "leads_generated", "client_since", "active"]
    ordering = ("-created",)
