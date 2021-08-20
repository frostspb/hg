from rest_framework import serializers
from django.conf import settings
from ..models import Campaign, TargetSection, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection, Teams
from hourglass.references.models import Tactics
from hourglass.references.api.serializers import JobTitlesSerializer, ITCuratedSerializer,\
    BANTQuestionSerializer, BANTAnswerSerializer, CustomQuestionSerializer, CustomAnswerSerializer, ManagersSerializer,\
    IntegrationTypeSerializer, CampaignTypesSerializer, PacingSerializer, AssociatesSerializer, CompanyRefSerializer
from hourglass.clients.api.serializers import ClientSerializer, CompanySerializer


class CampaignCopySerializer(serializers.Serializer):

    def save(self, **kwargs):
        campaign = self.context.get('campaign')
        return Campaign.objects.copy(campaign)


class TargetSectionSerializer(serializers.ModelSerializer):
    remaining_leads = serializers.SerializerMethodField()
    percent_completion = serializers.SerializerMethodField()
    type_name = serializers.CharField(source='campaign_pos_type')

    class Meta:
        model = TargetSection
        fields = (
            'type_name',
            'leads_goal', 'leads_generated', 'velocity', 'percent_completion', 'remaining_leads', 'grade',
        )

    def get_percent_completion(self, instance):
        return instance.percent_completion

    def get_remaining_leads(self, instance):
        return instance.remaining_leads


class SectionsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSettings
        ordering = ('-pos',)
        fields = (
            "id", "name", "slug", "enabled", "can_enabled", "delta_v_sector", "delta_v_per_row"
        )


class TacticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tactics
        fields = (
            "id", "name",
        )


class AssetsSectionSerializer(serializers.ModelSerializer):
    titles = JobTitlesSerializer(allow_null=True, many=True)
    landing_page = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AssetsSection
        fields = (
            "id", "name", "landing_page",  "percent", "campaign", "titles", "state"
        )

    def get_landing_page(self, instance):

        if instance.landing_page:
            photo_url = instance.landing_page.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


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


class JobTitlesSectionSerializer(serializers.ModelSerializer):
    job_title = JobTitlesSerializer(many=False)
    leads_generated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobTitlesSection
        fields = (
            "id", "job_title", "campaign",   "leads_generated", "state", "percent", "goal",
        )

    def get_leads_generated(self, instance):
        return instance.leads_generated


class IndustriesSectionSerializer(serializers.ModelSerializer):
    leads_industry = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(source='industry')

    class Meta:
        model = IndustriesSection
        fields = (
            "id", "name", "campaign", "leads_industry", "state", "percent",
        )

    def get_leads_industry(self, instance):
        return instance.leads_industry


class RevenueSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='revenue')
    leads_revenue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RevenueSection
        fields = (
            "id", "name", "campaign", "leads_revenue", "state", "percent",

        )

    def get_leads_revenue(self, instance):
        return instance.leads_revenue


class CompanySizeSectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='company_size')
    leads_company_size = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanySizeSection
        fields = (
            "id", "name", "campaign", "leads_company_size", "state", "percent",
        )

    def get_leads_company_size(self, instance):
        return instance.leads_company_size


class GeolocationsSectionSerializer(serializers.ModelSerializer):
    leads_geolocation = serializers.SerializerMethodField(read_only=True)

    name = serializers.CharField(source='geolocation')
    code = serializers.CharField(source='geolocation')

    class Meta:
        model = GeolocationsSection
        fields = (
            "id", "name", "geolocation", "campaign", "goal_per_geo" , "leads_geolocation",
            "name", "code", "state", "percent"
        )

    def get_leads_geolocation(self, instance):
        return instance.leads_geolocation


class BANTQuestionsSectionSerializer(serializers.ModelSerializer):
    question = BANTQuestionSerializer()
    answer = BANTAnswerSerializer()

    class Meta:
        model = BANTQuestionsSection
        fields = (
            "id", "campaign", "question", "answer", "question_txt", "answer_txt"
        )


class CustomQuestionsSectionSerializer(serializers.ModelSerializer):
    question = CustomQuestionSerializer()
    answer = CustomAnswerSerializer()

    class Meta:
        model = CustomQuestionsSection
        fields = (
            "id", "state", "campaign", "question", "answer", "question_txt", "answer_txt"
        )


class ABMSectionSerializer(serializers.ModelSerializer):
    #leads = serializers.SerializerMethodField(read_only=True)
    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ABMSection
        fields = (
            "id", "campaign", "title", "accounts_value", "file", "state", "percent",
        )

    #def get_leads(self, instance):
    #    return instance.leads

    def get_file(self, instance):
        if instance.file:

            photo_url = instance.file.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class InstallBaseSectionSerializer(serializers.ModelSerializer):
    leads_installbase = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InstallBaseSection
        fields = (
            "id",  "campaign", "name",  "leads_installbase", "state", "percent"
        )

    def get_leads_installbase(self, instance):
        return instance.leads_installbase


class FairTradeSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FairTradeSection
        fields = (
            "id",  "campaign", "name", "value", "state",
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


class NurturingSectionSerializer(serializers.ModelSerializer):

    assets = AssetsSectionSerializer()
    link = serializers.SerializerMethodField(read_only=True)
    generated_leads = serializers.SerializerMethodField(read_only=True)
    campaign_type = CampaignTypesSerializer()

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
        )

    def get_link(self, instance):
        return instance.link

    def get_generated_leads(self, instance):
        return instance.generated_leads


class CreativesSectionSerializer(serializers.ModelSerializer):
    landing_page = serializers.SerializerMethodField(read_only=True)
    banners = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CreativesSection
        fields = (
            "id", "subject_line", "email_text", "landing_page", "banners"
        )

    def get_email_text(self, instance):
        if instance.email_text:
            return instance.email_text

    def get_banners(self, instance):
        if instance.banners:

            photo_url = instance.banners.url
            return f"{settings.STORAGE_ADDR}{photo_url}"

    def get_landing_page(self, instance):
        if instance.landing_page:

            photo_url = instance.landing_page.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class ITCuratedSectionSerializer(serializers.ModelSerializer):
    curated = ITCuratedSerializer()

    class Meta:
        model = ITCuratedSection
        fields = (
            "id", "curated", "status", "pos"
        )


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

    class Meta:
        model = Teams
        fields = (
            "id",  "name", "team_lead", "team_member1", "team_member2",
            "team_member3", "team_member4", "delivered", "rejected",
        )

#TODO 1 serializer
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


    class Meta:
        model = Campaign
        fields = (
            "id", "client",
            "created", "active", "customer_information", "contact_name", "email", "note",
            "name", "campaign_type", "order", "managed_by", "targets", "sections",
            "delivered", "remaining", "in_validation", "total_generated", "audience_targeted",
            "start_date", "end_date", "kind", "dashboard_string_count", "ta_volume",
            "state",  "details",   "guarantees", "integration_type", "pacing_type", "assets", "intents",
            "artificial_titles", "titles",
            "industries", "revenues", "companies_size", "geolocations", "bants", "custom_questions", "abms",
            "install_base", "fair_trades", "lead_cascades", "nurturings", "nurturing_parameters", "creatives",
            "itcurateds",
            "abm_look_a_like", "rejected", "teams", "tactics",
            "intent_feed_goal_percent",  "intent_feed_done_percent", "abm_goal_percent", "goal_abm", "done_abm", "suppression_list",
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
            self.instance.end_date = datetime.strptime(self.initial_data['end_date'], settings.ENDPOINT_DATE_FORMAT)
            self.instance.save()

        if 'start_date' in self.initial_data:
            self.instance.end_date = datetime.strptime(self.initial_data['start_date'], settings.ENDPOINT_DATE_FORMAT)
            self.instance.save()

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

    class Meta:
        model = Campaign
        fields = (
            "end_date", "TA", "duration", "state", "velocity", "ta_volume", "pacing_type", "integration_type", "managed_by",
            "delivered", "remaining", "in_validation", "total_generated", "targets",
            "kind", "total_goal", "generated", "generated_pos", "sections", "tactics", "dashboard_string_count",
            "assets", "intents",  "artificial_titles","titles", "industries", "revenues", "companies_size", "geolocations",
            "bants", "custom_questions", "abms", "install_base", "fair_trades", "lead_cascades",
            "nurturings", "nurturing_parameters", "creatives", "itcurateds", "audience_targeted",
            "abm_look_a_like", "rejected", "teams", "intent_feed_goal_percent",
            "intent_feed_done_percent", "abm_goal_percent", "goal_abm", "done_abm", "suppression_list",
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

    class Meta:
        model = Campaign
        fields = (
            "client", "start_date", "created" , "end_date", "name", "integration_type",  "pacing_type", "targets", "tactics",
            "delivered", "remaining", "in_validation", "total_generated", "audience_targeted", "sections",
            "assets", "intents", "artificial_titles", "titles", "industries", "revenues", "companies_size", "geolocations",
            "bants", "custom_questions", "abms", "install_base", "fair_trades", "lead_cascades",
            "nurturings", "nurturing_parameters", "creatives", "abm_look_a_like","rejected", "teams",
            "intent_feed_goal_percent",  "intent_feed_done_percent", "abm_goal_percent","goal_abm", "done_abm",
            "suppression_list", "velocity"

        )

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

