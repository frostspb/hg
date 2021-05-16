from django.contrib import admin

from .models import CampaignTypes, Geolocations, Tactics #,JobTitles,


@admin.register(CampaignTypes)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(Geolocations)
class GeolocationsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", ]
    ordering = ("name",)


@admin.register(Tactics)
class TacticsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", ]
    ordering = ("name",)