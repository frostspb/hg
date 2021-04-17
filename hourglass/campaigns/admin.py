from django.contrib import admin
from .models import CampaignTemplate, CampaignTemplatePos, CampaignTypes, CampaignStandard, CampaignPos


class CampaignTemplatePosAdmin(admin.TabularInline):
    model = CampaignTemplatePos
    extra = 0


class CampaignPosAdmin(admin.TabularInline):
    model = CampaignPos
    extra = 0


@admin.register(CampaignTypes)
class CampaignTypesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name", "id"]
    fields = ["name", "active"]
    ordering = ("name",)


@admin.register(CampaignTemplate)
class CampaignTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "created", "active"]
    search_fields = ["client__name", "id"]
    fields = ["id", "client", "created", "active", "start_offset", "end_offset", "audience_targeted"]
    readonly_fields = ["id", "created", ]
    ordering = ("-created",)
    inlines = [CampaignTemplatePosAdmin]


@admin.register(CampaignStandard)
class CampaignStandardAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "created", "active"]
    search_fields = ["client__name", "id"]
    fields = ["id", "client", "created", "active", "start_offset", "end_offset", "audience_targeted"]
    readonly_fields = ["id", "created", ]
    ordering = ("-created",)
    inlines = [CampaignPosAdmin]
