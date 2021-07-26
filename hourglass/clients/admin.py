from django.contrib import admin

from .models import Client, Company


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = [
        "id", "name", "client_type", "client_since",
        "current_campaigns", "current_leads_goals",  "active", "created"
    ]
    search_fields = ["name", "id"]
    fields = ["name", "client_type", "total_campaigns", "leads_generated", "client_since", "active"]
    ordering = ("-created",)

    def current_campaigns(self, obj):
        return obj.current_campaigns

    def current_leads_goals(self, obj):
        return obj.current_leads_goals


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = [
        "id", "name", "client", "created"
    ]
    search_fields = ["name", "id"]
    fields = ["name", "client"]
    ordering = ("-created",)
