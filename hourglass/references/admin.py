from django.contrib import admin

from .models import CampaignTypes, Geolocations, Tactics, Question, Answers, Managers #,JobTitles,


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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "kind"]
    search_fields = ["name", "id"]


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]


@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "photo"]

