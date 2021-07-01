from django.contrib import admin

from .models import CampaignTypes, Geolocations, Tactics, Question, Answers, Managers, JobTitles,\
    ITCurated, Revenue, Industry, CompanySize


@admin.register(CampaignTypes)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(CompanySize)
class CompanySizeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(JobTitles)
class JobTitlesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(ITCurated)
class ITCuratedAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "link", "slug", "visible", ]
    search_fields = ["title", "id", "slug"]
    fields = ["title", "link", "slug", "visible",]
    ordering = ("title",)


@admin.register(Geolocations)
class GeolocationsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]
    search_fields = ["name", "id"]
    fields = ["name", "code"]
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

