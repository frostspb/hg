from django.http import Http404
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from model_clone import CloneModelAdmin
from django.contrib import admin, messages
from .models import Campaign, TargetSection, AssetsSection, IntentFeedsSection, JobTitlesSection,\
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, SectionSettings, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection



class SectionSettingsAdmin(admin.TabularInline):
    model = SectionSettings
    extra = 0
    fields = ['enabled', 'can_enabled', 'delta_ta_sector', 'delta_ta_per_row', 'delta_v_sector', 'delta_v_per_row']

    def has_add_permission(self, request, obj=None):
        return False


class TargetSectionAdmin(admin.TabularInline):
    model = TargetSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'velocity']
    fields = [ 'state', 'campaign_pos_type', 'leads_goal', 'leads_generated', 'percent_completion', 'remaining_leads']
    readonly_fields = ['percent_completion', 'remaining_leads']

    def percent_completion(self, obj):
        return obj.percent_completion

    def remaining_leads(self, obj):
        return obj.remaining_leads


class AssetsSectionAdmin(admin.TabularInline):
    model = AssetsSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    fields = ['state', 'name', 'landing_page', 'titles', 'leads_assets', 'percent']
    readonly_fields = ['leads_assets', ]

    def leads_assets(self, obj):
        return obj.leads_assets


class ITCuratedSectionAdmin(admin.TabularInline):
    model = ITCuratedSection
    extra = 0


class NurturingSectionAdmin(admin.TabularInline):
    model = NurturingSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    fields = ['state', 'name', 'assets', 'link', 'generated_leads']
    readonly_fields = ['generated_leads', 'link']

    def generated_leads(self, obj):
        return obj.generated_leads

    def link(self, obj):
        return obj.link


class CreativesSectionAdmin(admin.TabularInline):
    model = CreativesSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'state']


class SuppresionListSectionAdmin(admin.TabularInline):
    model = SuppresionListSection
    extra = 0
    exclude = ['execution_time', 'started_at']


class FairTradeSectionAdmin(admin.TabularInline):
    model = FairTradeSection
    extra = 0
    exclude = ['execution_time', 'started_at']


class ABMSectionAdmin(admin.TabularInline):
    model = ABMSection
    extra = 0
    fields = ['state', 'percent', 'file', 'accounts', 'goal_abm', ]
    readonly_fields = ['goal_abm',]
    exclude = ['name']

    def goal_abm(self, obj):
        return obj.goal_abm


class LeadCascadeProgramSectionAdmin(admin.TabularInline):
    model = LeadCascadeProgramSection
    extra = 0
    fields = ['state', 'percent', 'name',  'leads_cascade', ]
    readonly_fields = ['leads_cascade',]

    def leads_cascade(self, obj):
        return obj.leads_cascade


class InstallBaseSectionAdmin(admin.TabularInline):
    model = InstallBaseSection
    extra = 0
    fields = ['state', 'percent', 'name', 'leads_installbase', ]
    readonly_fields = ['leads_installbase', ]

    def leads_installbase(self, obj):
        return obj.leads_installbase


class IntentFeedsSectionAdmin(admin.TabularInline):
    model = IntentFeedsSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']
    fields = ['state', 'percent', 'name',   'company', 'kind', 'companies_count']
    readonly_fields = [ ]


class JobTitlesSectionAdmin(admin.TabularInline):
    model = JobTitlesSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']
    fields = ['state', 'percent', 'job_title', 'leads_generated', 'goal']
    readonly_fields = ['leads_generated', ]

    def leads_generated(self, obj):
        return obj.leads_generated


class IndustriesSectionAdmin(admin.TabularInline):
    model = IndustriesSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']
    fields = ['state', 'percent', 'name', 'leads_industry', ]
    readonly_fields = ['leads_industry', ]

    def leads_industry(self, obj):
        return obj.leads_industry


class GeolocationsSectionAdmin(admin.TabularInline):
    model = GeolocationsSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']

    fields = ['state', 'percent', 'name', 'leads_geolocation', 'geolocation' ]
    readonly_fields = ['leads_geolocation', ]

    def leads_geolocation(self, obj):
        return obj.leads_geolocation


class RevenueSectionAdmin(admin.TabularInline):
    model = RevenueSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']

    fields = ['state', 'percent', 'name', 'leads_revenue', ]
    readonly_fields = ['leads_revenue', ]

    def leads_revenue(self, obj):
        return obj.leads_revenue


class CompanySizeSectionAdmin(admin.TabularInline):
    model = CompanySizeSection
    extra = 0
    #exclude = ['execution_time', 'started_at', 'velocity']
    fields = ['state', 'percent', 'name', 'leads_company_size', ]
    readonly_fields = ['leads_company_size', ]

    def leads_revenue(self, obj):
        return obj.leads_revenue


class BANTQuestionsSectionAdmin(admin.TabularInline):
    model = BANTQuestionsSection
    extra = 0


class CustomQuestionsSectionAdmin(admin.TabularInline):
    model = CustomQuestionsSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'velocity']


@admin.register(Campaign)
class CampaignAdmin(CloneModelAdmin):
    list_display = [
        "id", "name_link", "client",  "created", "active",  "customer_information", "state", "ta", "velocity", "duration",
        "total_goal", "generated", "start_date_admin", "end_date_admin",
    ]
    search_fields = ["client__name", "id"]

    fieldsets = (
        ("Customer", {"fields": ("customer_information", "managed_by", "client")}),
        ("Campaign admin settings", {
            "fields": (
                "name", "start_offset", "end_offset",   "state", "job_titles"
                "base_velocity", "top_percent", "middle_percent", "bottom_percent", "tactics", "integration", "pacing",
                "dashboard_string_count", "remaining_admin_percent", "in_progress_admin_percent",
                "intent_feed_lead_generated", "intent_feed_goal_percent", "goal_intent_feed"
            )
        }),

        (
            "Target Audience",
            {"fields": ("audience_targeted", "delivered", "remaining", "in_validation")}
         )


    )

    readonly_fields = ["id", "created", "kind", "delivered", "remaining", "in_validation", "goal_intent_feed"]
    ordering = ("-created",)
    actions = ["start", "stop", "pause", "resume",]
    inlines = [
        SectionSettingsAdmin,
        TargetSectionAdmin,
        AssetsSectionAdmin,
        IntentFeedsSectionAdmin,
        ABMSectionAdmin,
        SuppresionListSectionAdmin,
        JobTitlesSectionAdmin,
        IndustriesSectionAdmin,
        GeolocationsSectionAdmin,
        RevenueSectionAdmin,
        CompanySizeSectionAdmin,
        BANTQuestionsSectionAdmin,
        CustomQuestionsSectionAdmin,
        InstallBaseSectionAdmin,
        ITCuratedSectionAdmin,
        LeadCascadeProgramSectionAdmin,
        FairTradeSectionAdmin,
        NurturingSectionAdmin,
        CreativesSectionAdmin,
    ]

    def goal_intent_feed(self, obj):
        return obj.goal_intent_feed

    def name_link(self, obj):
        url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.name)

    name_link.short_description = "Campaign Name"

    def delivered(self, obj):
        return obj.delivered

    def remaining(self, obj):
        return obj.remaining

    def in_validation(self, obj):
        return obj.in_validation

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

