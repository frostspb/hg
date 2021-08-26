from django.http import Http404
from django.urls import reverse
from django.utils.html import format_html
from model_clone import CloneModelAdmin
from django.contrib import admin
from ajax_select import make_ajax_form
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Campaign, TargetSection, AssetsSection, IntentFeedsSection, JobTitlesSection,\
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, SectionSettings, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection, \
    Teams, CampaignClient


class ComponentInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that sum of components is 100%"""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        total_sum = sum(form.cleaned_data.get('percent', 0) for form in self.forms)
        if total_sum > 100:
            raise ValidationError('Sum of components must be  less than or equal to 100%')


class SectionSettingsAdmin(admin.TabularInline):
    model = SectionSettings
    extra = 0
    fields = [
        'enabled', 'delta_ta_sector', 'delta_ta_per_row', 'delta_v_sector', 'delta_v_per_row',
        'quality_sector', 'quality_per_row', 'pos'
    ]
    classes = ['collapse']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class TargetSectionAdmin(admin.TabularInline):
    model = TargetSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'velocity']
    fields = [ 'state', 'campaign_pos_type', 'grade', 'leads_goal', 'leads_generated', 'percent_completion', 'remaining_leads']
    readonly_fields = ['percent_completion', 'remaining_leads']

    def percent_completion(self, obj):
        return obj.percent_completion

    def remaining_leads(self, obj):
        return obj.remaining_leads

    classes = ['collapse']


class AssetsSectionAdmin(admin.TabularInline):
    model = AssetsSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    fields = ['state', 'name', 'landing_page', 'titles', 'leads_assets', 'percent']
    readonly_fields = ['leads_assets', ]
    form = make_ajax_form(AssetsSection, {
        'titles': 'titles',  # ManyToManyField

    })
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_assets(self, obj):
        return obj.leads_assets


class ITCuratedSectionAdmin(admin.TabularInline):
    model = ITCuratedSection
    extra = 0
    classes = ['collapse']


class NurturingSectionAdmin(admin.TabularInline):
    model = NurturingSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    fields = ['state', 'campaign_type', 'assets', 'link', 'generated_leads', 'lead_goal']
    readonly_fields = ['generated_leads', 'link']
    classes = ['collapse']
    insert_after = "nurturing_parameters"

    def generated_leads(self, obj):
        return obj.generated_leads

    def link(self, obj):
        return obj.link


class CreativesSectionAdmin(admin.TabularInline):
    model = CreativesSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'state']
    classes = ['collapse']


class SuppresionListSectionAdmin(admin.TabularInline):
    model = SuppresionListSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    classes = ['collapse']


class FairTradeSectionAdmin(admin.TabularInline):
    model = FairTradeSection
    extra = 0
    exclude = ['execution_time', 'started_at']
    classes = ['collapse']


class ABMSectionAdmin(admin.TabularInline):
    model = ABMSection
    extra = 0
    exclude = ['execution_time', 'started_at', 'name']
    classes = ['collapse']

    insert_after = 'done_abm_percent'


class LeadCascadeProgramSectionAdmin(admin.TabularInline):
    model = LeadCascadeProgramSection
    extra = 0
    fields = ['state', 'percent', 'name',  'leads_cascade', ]
    readonly_fields = ['leads_cascade',]
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_cascade(self, obj):
        return obj.leads_cascade


class InstallBaseSectionAdmin(admin.TabularInline):
    model = InstallBaseSection
    extra = 0
    fields = ['state', 'percent', 'name', 'leads_installbase', ]
    readonly_fields = ['leads_installbase', ]
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_installbase(self, obj):
        return obj.leads_installbase


class IntentFeedsSectionAdmin(admin.TabularInline):
    model = IntentFeedsSection
    extra = 0
    fields = ['kind', 'state', 'name', 'companies_count',  'company',  'leads_generated', 'percent',  ]
    readonly_fields = ['leads_generated']
    classes = ['collapse']
    insert_after = 'total_intent_feed_aberdeen'
    formset = ComponentInlineFormSet
    form = make_ajax_form(IntentFeedsSection, {
        'company': 'company_ref',  # ManyToManyField

    })

    def leads_generated(self, obj):
        return obj.leads_generated


class JobTitlesSectionAdmin(admin.TabularInline):
    model = JobTitlesSection
    extra = 0
    fields = ['state', 'job_title', 'leads_generated', 'goal', 'percent', ]
    readonly_fields = ['leads_generated', ]
    classes = ['collapse']
    formset = ComponentInlineFormSet
    insert_after = "job_titles"

    def leads_generated(self, obj):
        return obj.leads_generated


class IndustriesSectionAdmin(admin.TabularInline):
    model = IndustriesSection
    extra = 0
    fields = ['state', 'industry', 'leads_industry',  'percent', ]
    readonly_fields = ['leads_industry', ]
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_industry(self, obj):
        return obj.leads_industry

    leads_industry.short_description = "Leads Generated"


class GeolocationsSectionAdmin(admin.TabularInline):
    model = GeolocationsSection
    extra = 0
    classes = ['collapse']
    fields = ['state', 'percent', 'name', 'goal_per_geo', 'leads_geolocation', 'geolocation',]
    readonly_fields = ['leads_geolocation', ]
    formset = ComponentInlineFormSet

    def leads_geolocation(self, obj):
        return obj.leads_geolocation


class RevenueSectionAdmin(admin.TabularInline):
    model = RevenueSection
    extra = 0
    fields = ['state',  'revenue', 'leads_revenue', 'percent',]
    readonly_fields = ['leads_revenue', ]
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_revenue(self, obj):
        return obj.leads_revenue

    leads_revenue.short_description = "Leads Generated"


class CompanySizeSectionAdmin(admin.TabularInline):
    model = CompanySizeSection
    extra = 0
    fields = ['state',  'company_size', 'leads_company_size', 'percent']
    readonly_fields = ['leads_company_size', ]
    classes = ['collapse']
    formset = ComponentInlineFormSet

    def leads_company_size(self, obj):
        return obj.leads_company_size

    leads_company_size.short_description = "Leads Generated"


class TeamsAdmin(admin.TabularInline):
    model = Teams
    extra = 0

    exclude = ['__all__']
    insert_after = 'generated_leads'


class BANTQuestionsSectionAdmin(admin.TabularInline):
    model = BANTQuestionsSection
    extra = 0
    classes = ['collapse']
    exclude = ['question_txt', 'answer_txt']
    fields = ['question', 'answer', 'kind',]
    readonly_fields = ['kind', ]

    def kind(self, obj):
        return obj.question.kind


class CustomQuestionsSectionAdmin(admin.TabularInline):
    model = CustomQuestionsSection
    extra = 0
    exclude = ['question_txt', 'answer_txt', 'started_at', 'execution_time']
    classes = ['collapse']


######## USER CAMPAIGN ################

@admin.register(CampaignClient)
class CampaignClientAdmin(CloneModelAdmin):

    list_display = [
        "id", "name_link", "client", "created", "active", "customer_information", "state",
        "start_date", "end_date",
    ]
    search_fields = ["client__name", "id"]

    fieldsets = (
        ("Customer", {"fields": ("customer_information", "managed_by", "client", "owner", "order", "details",
                                 "guarantees", "email", "note" )}),

        ("Intent Feed Total settings", {
            "fields": (
                "intent_feed_goal_percent", "intent_feed_done_percent", "goal_intent_feed", "done_intent_feed",
                "total_intent_feed", "total_intent_feed_infusemedia", "total_intent_feed_bombora",
                "total_intent_feed_aberdeen",
            )
        }
         ),

        ("ABM Total settings", {
            "fields": (
                "abm_goal_percent", "goal_abm", "done_abm", "done_abm_percent", "abm_look_a_like"

            )
        }
         ),

        ("Nurturing settings", {
            "fields": (
                "nurturing_parameters",

            )
        }
         ),
        ("Job Titles", {
            "fields": (
                "job_titles",

            )
        }
         ),

        (
            "Target Audience",
            {"fields": ("audience_targeted", "delivered", "remaining", "in_validation")}
        ),

        (
            "Lets Verify",
            {"fields": ("rejected", "total_goal", "generated_leads")}
        )
    )

    readonly_fields = [
        "id", "created", "kind", "delivered", "remaining", "in_validation", "goal_intent_feed",
        "generated_leads", "total_goal",
        "done_intent_feed", "total_intent_feed_bombora", "total_intent_feed_aberdeen", "total_intent_feed_infusemedia",
        "total_intent_feed", "goal_abm", "done_abm", "done_abm_percent"
    ]

    ordering = ("-created",)

    actions = ["start", "pause", ]

    inlines = [
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
        TeamsAdmin,
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(CampaignClientAdmin, self).get_queryset(request)
        qs = qs.filter(kind=Campaign.CampaignKinds.USER)
        return qs

    def goal_abm(self, obj):
        return obj.goal_abm

    def generated_leads(self, obj):
        return obj.generated_leads

    def done_abm(self, obj):
        return obj.done_abm

    def done_abm_percent(self, obj):
        return obj.done_abm_percent

    def total_intent_feed(self, obj):
        return obj.total_intent_feed

    def total_intent_feed_infusemedia(self, obj):
        return obj.total_intent_feed_infusemedia

    def total_intent_feed_bombora(self, obj):
        return obj.total_intent_feed_bombora

    def total_intent_feed_aberdeen(self, obj):
        return obj.total_intent_feed_aberdeen

    def goal_intent_feed(self, obj):
        return obj.goal_intent_feed

    def done_intent_feed(self, obj):
        return obj.done_intent_feed

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

    change_form_template = 'admin/custom/change_form.html'

    class Media:
        css = {
            'all': (
                'css/admin.css',
            )
        }


##########3 STANDARD CAMPAIGN ########

@admin.register(Campaign)
class CampaignAdmin(CloneModelAdmin):
    save_on_top = True
    form = make_ajax_form(Campaign, {
        'job_titles': 'titles_campaign',  # ManyToManyField

    })
    list_display = [
        "id", "name_link", "client",  "created", "active",  "customer_information", "state", "ta", "velocity", "duration",
        "total_goal", "generated", "start_date_admin", "end_date_admin",
    ]
    search_fields = ["client__name", "id"]

    fieldsets = (
        ("Customer", {"fields": ("customer_information", "managed_by", "client")}),
        ("Campaign admin settings", {
            "fields": (
                "name", "start_offset", "end_offset",   "state",
                "base_velocity", "top_percent", "middle_percent", "bottom_percent", "tactics", "integration_type",
                "pending",
                "pacing_type",

                "dashboard_string_count", "ta_volume", "remaining_admin_percent", "in_progress_admin_percent",


            )
        }),
        ("Intent Feed Total settings", {
            "fields": (
                "intent_feed_goal_percent", "intent_feed_done_percent", "goal_intent_feed", "done_intent_feed",
                "total_intent_feed", "total_intent_feed_infusemedia", "total_intent_feed_bombora",
                "total_intent_feed_aberdeen",
            )
        }
        ),

        ("ABM Total settings", {
            "fields": (
                "abm_goal_percent", "goal_abm", "done_abm", "done_abm_percent", "abm_look_a_like"

            )
        }
         ),

        ("Nurturing settings", {
            "fields": (
                "nurturing_parameters",

            )
        }
         ),
        ("Job Titles", {
            "fields": (
                "job_titles",

            )
        }
         ),

        (
            "Target Audience",
            {"fields": ("audience_targeted", "delivered", "remaining", "in_validation")}
         ),

        (
            "Lets Verify",
            {"fields": ("rejected", "total_goal", "generated_leads")}
        )
    )

    readonly_fields = [
        "id", "created", "kind", "delivered", "remaining", "in_validation", "goal_intent_feed",
        "generated_leads" ,"total_goal",
        "done_intent_feed", "total_intent_feed_bombora", "total_intent_feed_aberdeen", "total_intent_feed_infusemedia",
        "total_intent_feed", "goal_abm", "done_abm", "done_abm_percent"
    ]

    ordering = ("-created",)

    actions = ["start", "pause", ]

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
        TeamsAdmin,
    ]

    def get_queryset(self, request):
        qs = super(CampaignAdmin, self).get_queryset(request)
        qs = qs.filter(kind=Campaign.CampaignKinds.STANDARD)
        return qs

    def goal_abm(self, obj):
        return obj.goal_abm

    def generated_leads(self, obj):
        return obj.generated_leads

    def done_abm(self, obj):
        return obj.done_abm

    def done_abm_percent(self, obj):
        return obj.done_abm_percent

    def total_intent_feed(self, obj):
        return obj.total_intent_feed

    def total_intent_feed_infusemedia(self, obj):
        return obj.total_intent_feed_infusemedia

    def total_intent_feed_bombora(self, obj):
        return obj.total_intent_feed_bombora

    def total_intent_feed_aberdeen(self, obj):
        return obj.total_intent_feed_aberdeen

    def goal_intent_feed(self, obj):
        return obj.goal_intent_feed

    def done_intent_feed(self, obj):
        return obj.done_intent_feed

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

    change_form_template = 'admin/custom/change_form.html'

    class Media:
        css = {
            'all': (
                'css/admin.css',
            )
        }