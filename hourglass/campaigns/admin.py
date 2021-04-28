from django.http import Http404
from model_clone import CloneModelAdmin
from django.contrib import admin, messages
from .models import Campaign, CampaignsSection, AssetsSection, IntentFeedsSection, JobTitlesSection,\
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection


class CampaignsSectionAdmin(admin.TabularInline):
    model = CampaignsSection
    extra = 0


class AssetsSectionAdmin(admin.TabularInline):
    model = AssetsSection
    extra = 0


class IntentFeedsSectionAdmin(admin.TabularInline):
    model = IntentFeedsSection
    extra = 0


class JobTitlesSectionAdmin(admin.TabularInline):
    model = JobTitlesSection
    extra = 0


class IndustriesSectionAdmin(admin.TabularInline):
    model = IndustriesSection
    extra = 0


class RevenueSectionAdmin(admin.TabularInline):
    model = RevenueSection
    extra = 0


class GeolocationsSectionAdmin(admin.TabularInline):
    model = GeolocationsSection
    extra = 0


class CompanySizeSectionAdmin(admin.TabularInline):
    model = CompanySizeSection
    extra = 0


class BANTQuestionsSectionAdmin(admin.TabularInline):
    model = BANTQuestionsSection
    extra = 0


class CustomQuestionsSectionAdmin(admin.TabularInline):
    model = CustomQuestionsSection
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(CloneModelAdmin):
    list_display = [
        "id", "client", "created", "active",  "kind", "customer_information", "state",
    ]
    search_fields = ["client__name", "id"]
    fields = [
        "id", "client", "created", "active", "customer_information", "contact_name", "email", "note",
        "start_offset", "end_offset", "audience_targeted",
        "start_date", "end_date", "kind", "state", "settings"
    ]
    readonly_fields = ["id", "created", ]
    ordering = ("-created",)

    inlines = [
        CampaignsSectionAdmin,
        AssetsSectionAdmin,
        IntentFeedsSectionAdmin,
        JobTitlesSectionAdmin,
        IndustriesSectionAdmin,
        RevenueSectionAdmin,
        GeolocationsSectionAdmin,
        CompanySizeSectionAdmin,
        BANTQuestionsSectionAdmin,
        CustomQuestionsSectionAdmin,
    ]
