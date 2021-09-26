from django.contrib import admin

from .models import CampaignTypes, Geolocations, Tactics, Managers, JobTitles,\
    ITCurated, Revenue, Industry, CompanySize, BANTQuestion, BANTAnswer, CustomQuestion, CustomAnswer,\
    IntegrationType, Pacing, Associates, CompanyRef, NurturingStages


@admin.register(CampaignTypes)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(NurturingStages)
class NurturingStagesAdmin(admin.ModelAdmin):
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
    fields = ["title", "link", "slug", "visible", "position"]
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


@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "photo"]


class BANTAnswerAdmin(admin.TabularInline):
    model = BANTAnswer
    extra = 0
    fields = [
        'answer', 'preferred',
    ]


@admin.register(BANTQuestion)
class BANTQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question"]
    fields = ["question", "kind"]

    inlines = [BANTAnswerAdmin]


class CustomAnswerAdmin(admin.TabularInline):
    model = CustomAnswer
    extra = 0
    fields = [
        'answer', 'preferred',
    ]


@admin.register(CustomQuestion)
class CustomQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question"]
    fields = ["question"]

    inlines = [CustomAnswerAdmin]


@admin.register(IntegrationType)
class IntegrationTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name", "image", "image_popup"]


@admin.register(Pacing)
class PacingAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name", ]


@admin.register(CompanyRef)
class CompanyRefAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name", ]


@admin.register(Associates)
class AssociatesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name", "image", ]
