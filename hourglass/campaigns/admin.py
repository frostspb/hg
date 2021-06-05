from django.http import Http404
from model_clone import CloneModelAdmin
from django.contrib import admin, messages
from .models import Campaign, TargetSection, AssetsSection, IntentFeedsSection, JobTitlesSection,\
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, SectionSettings


class SectionSettingsAdmin(admin.TabularInline):
    model = SectionSettings
    extra = 0
    fields = ['enabled', 'can_enabled', 'delta_ta_sector', 'delta_ta_per_row', 'delta_v_sector', 'delta_v_per_row']

    def has_add_permission(self, request, obj=None):
        return False


class TargetSectionAdmin(admin.TabularInline):
    model = TargetSection
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
        "id", "client", "created", "active",  "customer_information", "state", "ta", "velocity", "duration",
        "total_goal", "generated", "start_date_admin", "end_date_admin"
    ]
    search_fields = ["client__name", "id"]

    fieldsets = (
        ("Customer", {"fields": ("customer_information", "managed_by", "client")}),
        ("Campaign admin settings", {
            "fields": (
                "name", "start_offset", "end_offset", "audience_targeted",  "state",
                "base_velocity", "top_percent", "middle_percent", "bottom_percent", "tactics", "integration", "pacing",
            )
        })

    )
    readonly_fields = ["id", "created", "kind"]
    ordering = ("-created",)
    actions = ["start", "stop", "pause", "resume",]
    inlines = [
        SectionSettingsAdmin,
        TargetSectionAdmin,
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

    def start_date_admin(self, obj):
        return obj.initial_start_date

    def end_date_admin(self, obj):
        return obj.initial_end_date

    def ta(self, obj):
        return obj.ta

    def velocity(self, obj):
        return obj.velocity

    def duration(self, obj):
        return obj.duration

    def total_goal(self, obj):
        return obj.total_goal

    def generated(self, obj):
        return obj.generated

    def pause(self, request, qs):
        if not request.user.is_staff:
            raise Http404

        for i in qs:
            i.pause()
            i.save()

    def resume(self, request, qs):
        if not request.user.is_staff:
            raise Http404

        for i in qs:
            i.resume()
            i.save()

    def stop(self, request, qs):
        if not request.user.is_staff:
            raise Http404

        for i in qs:
            i.stop()
            i.save()

    def start(self, request, qs):
        if not request.user.is_staff:
            raise Http404
        for i in qs:
            i.start()
            i.save()

