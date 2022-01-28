from rest_framework import serializers
from django.conf import settings
from ..models import Campaign, TargetSection, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection, Teams, Message,\
    CreativesBanner, CreativesLandingPage

from hourglass.references.models import Tactics, CampaignTypes, Geolocations, Revenue, Industry, NurturingStages, CompanyRef

from hourglass.references.api.serializers import JobTitlesSerializer, ITCuratedSerializer,\
    BANTQuestionSerializer, BANTAnswerSerializer, CustomQuestionSerializer, CustomAnswerSerializer, ManagersSerializer,\
    IntegrationTypeSerializer, CampaignTypesSerializer, PacingSerializer, AssociatesSerializer, CompanyRefSerializer, \
    NurturingStagesSerializer, PartOfMapSerializer, GeolocationsSerializer, RevenueSerializer, JobTitles

from hourglass.clients.api.serializers import ClientSerializer, CompanySerializer


class CampaignCopySerializer(serializers.Serializer):

    def save(self, **kwargs):
        campaign = self.context.get('campaign')
        return Campaign.objects.copy(campaign)


class TargetSectionCreateSerializer(serializers.ModelSerializer):
    pos_type_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    campaign_pos_type = serializers.PrimaryKeyRelatedField(queryset=CampaignTypes.objects.all(), required=False, allow_null=True, allow_empty=True)
    #campaign_pos_type = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = TargetSection
        fields = (
            'campaign_pos_type',
            'leads_goal',
            'grade',
            'pos_type_name', "state"
        )


class TargetSectionSerializer(serializers.ModelSerializer):
    remaining_leads = serializers.SerializerMethodField()
    percent_completion = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = TargetSection
        fields = (
            'type_name', 'campaign_pos_type',
            'leads_goal', 'leads_generated', 'velocity', 'percent_completion', 'remaining_leads', 'grade',
        )

    def get_percent_completion(self, instance):
        return instance.percent_completion

    def get_remaining_leads(self, instance):
        return instance.remaining_leads

    def get_type_name(self, instance):
        if instance.pos_type_name:
            return instance.pos_type_name
        else:
            return instance.campaign_pos_type.name


class SectionsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSettings
        ordering = ('-pos',)
        fields = (
            "id", "name", "slug", "enabled", "can_enabled", "delta_v_sector", "delta_v_per_row", "delta_ta_sector",
            "delta_ta_per_row", "quality_sector", "quality_per_row"
        )


class TacticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tactics
        fields = (
            "id", "name",
        )


class AssetsCreateSectionSerializer(serializers.ModelSerializer):
    landing_page = serializers.FileField(required=False, allow_null=True)
    titles = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=JobTitles.objects.all())

    class Meta:
        model = AssetsSection
        fields = (
             "name", "landing_page", "titles", "state", "percent"
        )


class AssetsSectionSerializer(serializers.ModelSerializer):
    titles = JobTitlesSerializer(allow_null=True, many=True)
    landing_page = serializers.SerializerMethodField(read_only=True)
    leads_assets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AssetsSection
        fields = (
            "id", "name", "landing_page",  "percent", "campaign", "titles", "state", "leads_assets",

        )

    def get_landing_page(self, instance):

        if instance.landing_page:
            photo_url = instance.landing_page.url
            return f"{settings.STORAGE_ADDR}{photo_url}"

    def get_leads_assets(self, instance):

        return instance.leads_assets


class IntentFeedsCreateSectionSerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=CompanyRef.objects.all(), required=False)

    class Meta:
        model = IntentFeedsSection
        fields = (
             "name", "company", "kind", "percent", "state", "industry"

        )


class IntentFeedsSectionSerializer(serializers.ModelSerializer):
    leads_generated = serializers.SerializerMethodField(read_only=True)
    goal_intent_feed = serializers.SerializerMethodField(read_only=True)
    company = CompanyRefSerializer(many=True)

    class Meta:
        model = IntentFeedsSection
        fields = (
            "id", "name", "campaign",  "company", "leads_generated", "kind", "percent", "goal_intent_feed",
            "companies_count", "state",
        )

    def get_leads_generated(self, instance):
        return instance.leads_generated

    def get_goal_intent_feed(self, instance):
        return instance.goal_intent_feed


class JobTitlesCreateSectionSerializer(serializers.ModelSerializer):
    user_job_title = serializers.CharField(required=False)

    class Meta:
        model = JobTitlesSection
        fields = (
             "job_title",  "goal", "user_job_title", "state",
        )


class JobTitlesSectionSerializer(serializers.ModelSerializer):
    job_title = JobTitlesSerializer(many=False)
    leads_generated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobTitlesSection
        fields = (
            "id", "job_title", "campaign",   "leads_generated", "state", "percent", "goal", "user_job_title"
        )

    def get_leads_generated(self, instance):
        return instance.leads_generated


class IndustriesSectionCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    user_industry = serializers.CharField(required=False)
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), required=False)

    class Meta:
        model = IndustriesSection
        fields = (
             "industry", "name", "user_industry", "state",

        )


class IndustriesSectionSerializer(serializers.ModelSerializer):
    leads_industry = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(source='industry')

    class Meta:
        model = IndustriesSection
        fields = (
            "id", "name", "campaign", "leads_industry", "state", "percent", "user_industry", "industry"
        )

    def get_leads_industry(self, instance):
        return instance.leads_industry


class RevenueSectionCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    user_revenue = serializers.CharField(required=False)
    revenue = serializers.PrimaryKeyRelatedField(queryset=Revenue.objects.all(), required=False)

    class Meta:
        model = RevenueSection
        fields = (
             "revenue", "name", "user_revenue", "state"

        )


class RevenueSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='revenue')
    leads_revenue = serializers.SerializerMethodField(read_only=True)
    revenue = RevenueSerializer()

    class Meta:
        model = RevenueSection
        fields = (
            "id", "name", "campaign", "leads_revenue", "state", "percent", "revenue", "user_revenue",

        )

    def get_leads_revenue(self, instance):
        return instance.leads_revenue


class CompanySizeCreateSectionSerializer(serializers.ModelSerializer):
    user_company_size = serializers.CharField(required=False)

    class Meta:
        model = CompanySizeSection
        fields = (
            "company_size", "user_company_size", "state"
        )


class CompanySizeSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='company_size')
    leads_company_size = serializers.SerializerMethodField(read_only=True)
    company_size = CompanySerializer()

    class Meta:
        model = CompanySizeSection
        fields = (
            "id", "name", "campaign", "leads_company_size", "state", "percent", "company_size", "user_company_size",
        )

    def get_leads_company_size(self, instance):
        return instance.leads_company_size


class GeolocationsCreateSectionSerializer(serializers.ModelSerializer):
    geolocation = serializers.PrimaryKeyRelatedField(queryset=Geolocations.objects.all(), required=False)
    goal_per_geo = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = GeolocationsSection
        fields = (
            "name", "geolocation", "user_geolocation", "state", "goal_per_geo"
        )


class GeolocationsSectionSerializer(serializers.ModelSerializer):
    leads_geolocation = serializers.SerializerMethodField(read_only=True)

    code = serializers.CharField(source='geolocation')
    geolocation = GeolocationsSerializer()

    class Meta:
        model = GeolocationsSection
        fields = (
            "id", "name", "geolocation", "campaign", "goal_per_geo" , "leads_geolocation",
            "code", "state", "percent", "user_geolocation"
        )

    def get_leads_geolocation(self, instance):
        return instance.leads_geolocation


class BANTQuestionsCreateSectionSerializer(serializers.ModelSerializer):
      class Meta:
        model = BANTQuestionsSection
        fields = (
            "question", "answer",
        )


class BANTQuestionsSectionSerializer(serializers.ModelSerializer):
    question = BANTQuestionSerializer()
    answer = BANTAnswerSerializer()

    class Meta:
        model = BANTQuestionsSection
        fields = (
            "id", "campaign", "question", "answer",
        )


class CustomQuestionsCreateSectionSerializer(serializers.ModelSerializer):

       class Meta:
        model = CustomQuestionsSection
        fields = (
            "question", "answer",  "state"
        )


class CustomQuestionsSectionSerializer(serializers.ModelSerializer):
    question = CustomQuestionSerializer()
    answer = CustomAnswerSerializer()

    class Meta:
        model = CustomQuestionsSection
        fields = (
            "id", "state", "campaign", "question", "answer",
        )


class ABMSectionCreateSerializer(serializers.ModelSerializer):

    file = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = ABMSection
        fields = (
            "title", "accounts_value", "file", "state"
        )


class ABMSectionSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ABMSection
        fields = (
            "id", "campaign", "title", "accounts_value", "file", "state", "percent",
        )


    def get_file(self, instance):
        if instance.file:

            photo_url = instance.file.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class InstallBaseCreateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallBaseSection
        fields = (
           "name", "state"
        )


class InstallBaseSectionSerializer(serializers.ModelSerializer):
    leads_installbase = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InstallBaseSection
        fields = (
            "id",  "campaign", "name",  "leads_installbase", "state", "percent"
        )

    def get_leads_installbase(self, instance):
        return instance.leads_installbase


class FairTradeCreateSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FairTradeSection
        fields = (
            "name", "value", "state"
        )


class FairTradeSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FairTradeSection
        fields = (
            "id",  "campaign", "name", "value", "state",
        )


class LeadCascadeProgramCreateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadCascadeProgramSection
        fields = (
             "name", "state"
        )


class LeadCascadeProgramSectionSerializer(serializers.ModelSerializer):
    leads_cascade = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadCascadeProgramSection
        fields = (
            "id", "campaign", "name", "percent", 'leads_cascade', "state",
        )

    def get_leads_cascade(self, instance):
        return instance.leads_cascade


class NurturingCreateSectionSerializer(serializers.ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(queryset=Campaign.objects.all())
    assets = serializers.PrimaryKeyRelatedField(queryset=AssetsSection.objects.all())
    campaign_type = serializers.PrimaryKeyRelatedField(queryset=CampaignTypes.objects.all())
    nurturing_stages = serializers.PrimaryKeyRelatedField(queryset=NurturingStages.objects.all())

    class Meta:
        model = NurturingSection
        fields = (
            "campaign",
            "campaign_type",
            "assets",
            "link",
            "nurturing_stages", "state",
        )


class NurturingSectionSerializer(serializers.ModelSerializer):

    assets = AssetsSectionSerializer()
    link = serializers.SerializerMethodField(read_only=True)
    generated_leads = serializers.SerializerMethodField(read_only=True)
    campaign_type = CampaignTypesSerializer()
    nurturing_stages = NurturingStagesSerializer()

    class Meta:
        model = NurturingSection
        fields = (
            "id",
            "campaign",
            "campaign_type",
            "assets",
            "link",
            "generated_leads",
            "state",
            "lead_goal",
            "nurturing_stages",
        )

    def get_link(self, instance):
        if instance.link:
            photo_url = instance.link.url
            return f"{settings.STORAGE_ADDR}{photo_url}"

    def get_generated_leads(self, instance):
        return instance.generated_leads


class CreativesSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreativesSection
        fields = (
            "subject_line", "email_text", "landing_page", "banners", "state"
        )


class CreativesBannersSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    class Meta:
        model = CreativesBanner
        fields = (
            "id", "banner",
        )

    def get_banner(self, instance):
        if instance.banner:
            photo_url = instance.banner.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class CreativesLandingPageSerializer(serializers.ModelSerializer):
    landing_page = serializers.SerializerMethodField()

    class Meta:
        model = CreativesLandingPage
        fields = (
            "id", "landing_page",
        )

    def get_landing_page(self, instance):
        if instance.landing_page:
            photo_url = instance.landing_page.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class CreativesSectionSerializer(serializers.ModelSerializer):


    class Meta:
        model = CreativesSection
        fields = (
            "id", "subject_line", "email_text",  "state"
        )

    def get_email_text(self, instance):
        if instance.email_text:
            return instance.email_text

    # def get_banners(self, instance):
    #     if instance.banners:
    #
    #         photo_url = instance.banners.url
    #         return f"{settings.STORAGE_ADDR}{photo_url}"
    #
    # def get_landing_page(self, instance):
    #     if instance.landing_page:
    #
    #         photo_url = instance.landing_page.url
    #         return f"{settings.STORAGE_ADDR}{photo_url}"


class ITCuratedSectionSerializer(serializers.ModelSerializer):
    curated = ITCuratedSerializer()

    class Meta:
        model = ITCuratedSection
        fields = (
            "id", "curated", "status", "pos"
        )


class ITCuratedUpdateStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()


class SettingsUpdateStatusSerializer(serializers.Serializer):
    slug = serializers.CharField()
    enabled = serializers.CharField()


class SuppresionListSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppresionListSection
        fields = (
            "id",  "campaign", "title", "accounts_value", "state",
        )


class TeamsSerializer(serializers.ModelSerializer):
    team_lead = AssociatesSerializer(read_only=True, many=False)
    team_member1 = AssociatesSerializer(read_only=True, many=False)
    team_member2 = AssociatesSerializer(read_only=True, many=False)
    team_member3 = AssociatesSerializer(read_only=True, many=False)
    team_member4 = AssociatesSerializer(read_only=True, many=False)
    delivered = serializers.SerializerMethodField(read_only=True)
    rejected = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Teams
        fields = (
            "id",  "name", "team_lead", "team_member1", "team_member2",
            "team_member3", "team_member4", "delivered", "rejected", "rejected_percent"
        )

    def get_delivered(self, instance):
        return instance.delivered

    def get_rejected(self, instance):
        return instance.rejected

#TODO 1 serializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name"]


class CampaignCreateSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(required=False)
    creatives = CreativesSectionCreateSerializer(many=True, allow_null=True, required=False)
    assets = AssetsCreateSectionSerializer(many=True, allow_null=True, required=False)
    intents = IntentFeedsCreateSectionSerializer(many=True, allow_null=True, required=False)
    industries = IndustriesSectionCreateSerializer(many=True, allow_null=True, required=False)
    revenues = RevenueSectionCreateSerializer(many=True, allow_null=True, required=False)
    titles = JobTitlesCreateSectionSerializer(many=True, allow_null=True, required=False)
    companies = CompanySizeCreateSectionSerializer(many=True, allow_null=True, required=False)
    targets = TargetSectionCreateSerializer(many=True, allow_null=True, required=False)
    geolocations = GeolocationsCreateSectionSerializer(many=True, allow_null=True, required=False)
    bants = BANTQuestionsCreateSectionSerializer(many=True, allow_null=True, required=False)
    cqs = CustomQuestionsCreateSectionSerializer(many=True, allow_null=True, required=False)
    abms = ABMSectionCreateSerializer(many=True, allow_null=True, required=False)
    ibs = InstallBaseCreateSectionSerializer(many=True, allow_null=True, required=False)
    fair_trades = FairTradeCreateSectionSerializer(many=True, allow_null=True, required=False)
    lead_cascades = LeadCascadeProgramCreateSectionSerializer(many=True, allow_null=True, required=False)
    #nurturings = NurturingCreateSectionSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Campaign
        fields = (
            "email", "client", "integration_type", "pacing_type", "name", "creatives", "assets",
            "intents", "industries", "revenues", "companies", "geolocations", "bants", "cqs", "abms",
            "ibs", "fair_trades", "lead_cascades", #"nurturings",
            "nurturing_parameters", "targets", "titles", "guarantees", "note", "details", "customer_information",
            "order", "contact_name", "end_date", "start_date", "kind", "part_of_the_map", "nurturing_parameters",
            "abm_look_a_like_state", "intent_feed_goal_percent", "intent_feed_done_percent", "abm_goal_percent", "id", "campaign_type",
            # "itcurateds",
            # "teams", "tactics",
            # "suppression_list",
            # "client", "abm_look_a_like_state",
            # "customer_information", "contact_name", "email", "note",
            # "name", "campaign_type", "order",  "targets",
            # "start_date", "end_date",
            # "state",  "details",   "guarantees", "integration_type", "pacing_type", "assets", "intents",
            # "artificial_titles", "titles",
            # "industries", "revenues", "companies_size", "geolocations", "bants", "custom_questions", "abms",
            # "install_base", "fair_trades", "lead_cascades", "nurturings", "nurturing_parameters", "creatives",
            # "itcurateds",
            # "teams", "tactics",
            # "suppression_list",
        )


class CampaignSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField() #
    created = serializers.SerializerMethodField()

    kind = serializers.CharField(default=Campaign.CampaignKinds.USER)

    remaining = serializers.SerializerMethodField() #
    in_validation = serializers.SerializerMethodField() #
    delivered = serializers.SerializerMethodField() #
    total_generated = serializers.SerializerMethodField() #

    integration_type = IntegrationTypeSerializer(allow_null=True, required=False) #
    pacing_type = PacingSerializer(allow_null=True, required=False) #

    teams = TeamsSerializer(read_only=True, many=True) #
    tactics = TacticsSerializer(read_only=True, many=True)
    sections = SectionsSettingsSerializer(read_only=True, many=True) #
    targets = TargetSectionSerializer(read_only=True, many=True) #

    assets = AssetsSectionSerializer(many=True, read_only=True) #
    intents = IntentFeedsSectionSerializer(many=True, read_only=True) #
    artificial_titles = JobTitlesSerializer(source='jt', many=True, read_only=True) #
    titles = JobTitlesSectionSerializer(many=True, read_only=True) #
    industries = IndustriesSectionSerializer(many=True, read_only=True) #
    revenues = RevenueSectionSerializer(many=True, read_only=True) #
    companies_size = CompanySizeSectionSerializer(source="companies", many=True, read_only=True) #
    geolocations = GeolocationsSectionSerializer(many=True, read_only=True) #
    bants = BANTQuestionsSectionSerializer(many=True, read_only=True) #
    custom_questions = CustomQuestionsSectionSerializer(source="cqs", many=True, read_only=True) #
    abms = ABMSectionSerializer(many=True, read_only=True) #
    install_base = InstallBaseSectionSerializer(source="ibs", many=True, read_only=True) #
    fair_trades = FairTradeSectionSerializer(many=True, read_only=True) #
    lead_cascades = LeadCascadeProgramSectionSerializer(many=True, read_only=True) #
    nurturings = NurturingSectionSerializer(many=True, read_only=True) #
    creatives = CreativesSectionSerializer(many=True, read_only=True) #
    itcurateds = ITCuratedSectionSerializer(many=True, read_only=True) #
    suppression_list = SuppresionListSectionSerializer(source='sups', many=True, read_only=True) #
    part_of_the_map = PartOfMapSerializer(allow_null=True, required=False)
    client_name = serializers.CharField(source='client.name', required=False)
    banners = CreativesBannersSerializer(many=True, read_only=True)
    landings = CreativesLandingPageSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = (
            "id", "client", "client_name", "abm_look_a_like_state",
            "created", "active", "pending","engagement_in_process_value","maximum_campaign_completeness","engagement_in_process",  "base_velocity", "base_quality", "customer_information", "contact_name", "email", "note",
            "name", "campaign_type", "order", "managed_by", "targets", "sections",
            "delivered", "remaining", "in_validation", "total_generated", "audience_targeted",
            "start_date", "end_date", "kind", "dashboard_string_count", "ta_volume",
            "state",  "details",   "guarantees", "integration_type", "pacing_type", "assets", "intents",
            "artificial_titles", "titles",
            "industries", "revenues", "companies_size", "geolocations", "bants", "custom_questions", "abms",
            "install_base", "fair_trades", "lead_cascades", "nurturings", "nurturing_parameters", "creatives",
            "itcurateds",
            "abm_look_a_like", "rejected", "teams", "tactics",
            "intent_feed_goal_percent",  "intent_feed_done_percent", "abm_goal_percent", "goal_abm", "done_abm",
            "suppression_list", "part_of_the_map", "landings", "banners"
        )
        read_only_fields = ['client_name']

    def get_goal_abm(self, instance):
        return instance.goal_abm

    def get_done_abm(self, instance):
        return instance.done_abm

    def get_delivered(self, instance):
        return instance.delivered

    def get_remaining(self, instance):
        return instance.remaining

    def get_in_validation(self, instance):
        return instance.in_validation

    def get_total_generated(self, instance):
        return instance.total_generated

    def get_created(self, instance):
        if instance.created:
            return instance.created.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_start_date(self, instance):
        res = None
        if instance.is_standard:
            if instance.initial_start_date:
                res = instance.initial_start_date
        else:
            if instance.start_date:
                res = instance.start_date
        if res:
            return res.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_end_date(self, instance):
        res = None
        if instance.is_standard:
            if instance.initial_end_date:
                res = instance.initial_end_date
        else:
            if instance.end_date:
                res = instance.end_date
        if res:
            return res.strftime(settings.ENDPOINT_DATE_FORMAT)

    def save(self, **kwargs):
        super().save(**kwargs)
        from datetime import datetime
        if 'end_date' in self.initial_data:
            try:
                self.instance.end_date = datetime.strptime(self.initial_data['end_date'], settings.ENDPOINT_DATE_FORMAT)
                self.instance.save()
            except:
                pass

        if 'start_date' in self.initial_data:
            try:
                self.instance.end_date = datetime.strptime(self.initial_data['start_date'], settings.ENDPOINT_DATE_FORMAT)
                self.instance.save()
            except:
                pass

        return self.instance


class HourglassSerializer(serializers.ModelSerializer):
    end_date = serializers.SerializerMethodField()

    delivered = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    in_validation = serializers.SerializerMethodField()
    total_generated = serializers.SerializerMethodField()

    integration_type = IntegrationTypeSerializer()
    pacing_type = PacingSerializer()

    TA = serializers.SerializerMethodField()

    duration = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    velocity = serializers.SerializerMethodField()
    total_goal = serializers.SerializerMethodField()
    generated = serializers.SerializerMethodField()
    generated_pos = serializers.SerializerMethodField()

    #tactics = TacticsSerializer(read_only=True, many=True)
    teams = TeamsSerializer(read_only=True, many=True)

    sections = SectionsSettingsSerializer(read_only=True, many=True)
    targets = TargetSectionSerializer(read_only=True, many=True)
    tactics = serializers.SerializerMethodField()

    managed_by = ManagersSerializer(read_only=True)

    assets = AssetsSectionSerializer(many=True, read_only=True)
    intents = IntentFeedsSectionSerializer(many=True, read_only=True)
    artificial_titles = JobTitlesSerializer(source='jt', many=True, read_only=True)
    titles = JobTitlesSectionSerializer(many=True, read_only=True)
    industries = IndustriesSectionSerializer(many=True, read_only=True)
    revenues = RevenueSectionSerializer(many=True, read_only=True)
    companies_size = CompanySizeSectionSerializer(source="companies", many=True, read_only=True)
    geolocations = GeolocationsSectionSerializer(many=True, read_only=True)
    bants = BANTQuestionsSectionSerializer(many=True, read_only=True)
    custom_questions = CustomQuestionsSectionSerializer(source="cqs", many=True, read_only=True)
    abms = ABMSectionSerializer(many=True, read_only=True)
    install_base = InstallBaseSectionSerializer(source="ibs", many=True, read_only=True)
    fair_trades = FairTradeSectionSerializer(many=True, read_only=True)
    lead_cascades = LeadCascadeProgramSectionSerializer(many=True, read_only=True)
    nurturings = NurturingSectionSerializer(many=True, read_only=True)
    creatives = CreativesSectionSerializer(many=True, read_only=True)
    itcurateds = ITCuratedSectionSerializer(many=True, read_only=True)
    suppression_list = SuppresionListSectionSerializer(source='sups', many=True, read_only=True)
    part_of_the_map = PartOfMapSerializer(allow_null=True, required=False)
    banners = CreativesBannersSerializer(many=True, read_only=True)
    landings = CreativesLandingPageSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = (
            "end_date", "TA", "base_velocity", "engagement_in_process_value","maximum_campaign_completeness", "engagement_in_process","pending",  "base_quality", "duration", "state", "velocity", "ta_volume", "pacing_type", "integration_type", "managed_by",
            "delivered", "remaining", "in_validation", "total_generated", "targets",
            "kind", "total_goal", "generated", "generated_pos", "sections", "tactics", "dashboard_string_count",
            "assets", "intents",  "artificial_titles","titles", "industries", "revenues", "companies_size", "geolocations",
            "bants", "custom_questions", "abms", "install_base", "fair_trades", "lead_cascades",
            "nurturings", "nurturing_parameters", "creatives", "itcurateds", "audience_targeted",
            "abm_look_a_like", "rejected", "teams", "intent_feed_goal_percent", "kind",
            "intent_feed_done_percent", "abm_goal_percent", "goal_abm", "done_abm", "suppression_list",
            "part_of_the_map","abm_look_a_like_state",  "landings", "banners",
        )

    def get_goal_abm(self, instance):
        return instance.goal_abm

    def get_done_abm(self, instance):

        return instance.done_abm

    def get_delivered(self, instance):
        return instance.delivered

    def get_remaining(self, instance):
        return instance.remaining

    def get_in_validation(self, instance):
        return instance.in_validation

    def get_total_generated(self, instance):
        return instance.total_generated

    def get_end_date(self, instance):
        if instance.kind == instance.CampaignKinds.STANDARD:
            return instance.initial_end_date.strftime(settings.ENDPOINT_DATE_FORMAT)

        if instance.end_date:
            return instance.end_date.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_TA(self, instance):
        return instance.ta

    def get_duration(self, instance):
        return instance.duration

    def get_state(self, instance):
        return instance.state

    def get_velocity(self, instance):
        return instance.velocity

    def get_total_goal(self, instance):
        return instance.total_goal

    def get_generated(self, instance):
        return instance.generated

    def get_generated_pos(self, instance):
        return instance.generated_pos

    def get_tactics(self, instance):
        model_tactics = instance.tactics.values_list('id', flat=True)
        t = Tactics.objects.all().values()
        for i in t:
            i['active'] = True if i.get('id') in model_tactics else False
        return t


class CampaignSettingsSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    client = ClientSerializer(read_only=True, many=False)
    TA = serializers.SerializerMethodField()
    targets = TargetSectionSerializer(read_only=True, many=True)
    tactics = serializers.SerializerMethodField()
    integration_type = IntegrationTypeSerializer()
    delivered = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    in_validation = serializers.SerializerMethodField()
    total_generated = serializers.SerializerMethodField()
    pacing_type = PacingSerializer()
    sections = SectionsSettingsSerializer(read_only=True, many=True)
    teams = TeamsSerializer(read_only=True, many=True)
    velocity = serializers.SerializerMethodField()
    assets = AssetsSectionSerializer(many=True, read_only=True)
    intents = IntentFeedsSectionSerializer(many=True, read_only=True)
    artificial_titles = JobTitlesSerializer(source='job_titles', many=True, read_only=True)
    titles = JobTitlesSectionSerializer(many=True, read_only=True)
    industries = IndustriesSectionSerializer(many=True, read_only=True)
    revenues = RevenueSectionSerializer(many=True, read_only=True)
    companies_size = CompanySizeSectionSerializer(source="companies", many=True, read_only=True)
    geolocations = GeolocationsSectionSerializer(many=True, read_only=True)
    bants = BANTQuestionsSectionSerializer(many=True, read_only=True)
    custom_questions = CustomQuestionsSectionSerializer(source="cqs", many=True, read_only=True)
    abms = ABMSectionSerializer(many=True, read_only=True)
    install_base = InstallBaseSectionSerializer(source="ibs", many=True, read_only=True)
    fair_trades = FairTradeSectionSerializer(many=True, read_only=True)
    lead_cascades = LeadCascadeProgramSectionSerializer(many=True, read_only=True)
    nurturings = NurturingSectionSerializer(many=True, read_only=True)
    creatives = CreativesSectionSerializer(many=True, read_only=True)
    suppression_list = SuppresionListSectionSerializer(source='sups', many=True, read_only=True)
    itcurateds = ITCuratedSectionSerializer(many=True, read_only=True)
    part_of_the_map = PartOfMapSerializer(allow_null=True, required=False)
    banners = CreativesBannersSerializer(many=True, read_only=True)
    landings = CreativesLandingPageSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = (
            "client", "TA", "base_velocity", "maximum_campaign_completeness", "engagement_in_process_value","pending","engagement_in_process", "base_quality",  "start_date", "created" , "end_date", "name", "integration_type",  "pacing_type", "targets", "tactics",
            "delivered", "remaining", "in_validation", "total_generated", "audience_targeted", "sections",
            "assets", "intents", "artificial_titles", "titles", "industries", "revenues", "companies_size", "geolocations",
            "bants", "custom_questions", "abms", "install_base", "fair_trades", "lead_cascades",
            "nurturings", "nurturing_parameters", "creatives", "abm_look_a_like","rejected", "teams",
            "intent_feed_goal_percent",  "intent_feed_done_percent", "abm_goal_percent","goal_abm",
            "done_abm", "itcurateds", "kind",
            "suppression_list", "velocity", "state", "part_of_the_map",
            "abm_look_a_like_state", "landings", "banners"

        )

    def get_TA(self, instance):
        return instance.ta

    def get_goal_abm(self, instance):
        return instance.goal_abm

    def get_done_abm(self, instance):
        return instance.done_abm

    def get_delivered(self, instance):
        return instance.delivered

    def get_velocity(self, instance):
        return instance.velocity

    def get_created(self, instance):
        if instance.created:
            return instance.created.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_remaining(self, instance):
        return instance.remaining

    def get_in_validation(self, instance):
        return instance.in_validation

    def get_total_generated(self, instance):
        return instance.total_generated

    def get_start_date(self, instance):
        res = None
        if instance.is_standard:
            if instance.initial_start_date:
                res = instance.initial_start_date
        else:
            if instance.start_date:
                res = instance.start_date
        if res:
            return res.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_end_date(self, instance):
        res = None
        if instance.is_standard:
            if instance.initial_end_date:
                res = instance.initial_end_date
        else:
            if instance.end_date:
                res = instance.end_date
        if res:
            return res.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_tactics(self, instance):
        model_tactics = instance.tactics.values_list('id', flat=True)
        t = Tactics.objects.all().values()
        for i in t:
            i['active'] = True if i.get('id') in model_tactics else False
        return t


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "campaign", "message", "manager")





