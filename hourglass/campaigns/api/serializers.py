from rest_framework import serializers
from django.conf import settings
from ..models import Campaign, TargetSection, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection,ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection
from hourglass.references.models import CampaignTypes, Tactics, JobTitles, Geolocations
from hourglass.references.api.serializers import JobTitlesSerializer, ITCuratedSerializer,\
    BANTQuestionSerializer, BANTAnswerSerializer, CustomQuestionSerializer, CustomAnswerSerializer
from hourglass.clients.api.serializers import ClientSerializer


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
        fields = (
            'id', 'name',
        )


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
            'leads_goal', 'leads_generated', 'velocity', 'percent_completion', 'remaining_leads'
        )

    def get_percent_completion(self, instance):
        return instance.percent_completion

    def get_remaining_leads(self, instance):
        return instance.remaining_leads





class SectionsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSettings
        ordering = ('-name',)
        fields = (
            "id", "name", "slug", "enabled", "can_enabled"
        )


class TacticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tactics
        fields = (
            "id", "name",
        )


class HourglassSerializer(serializers.ModelSerializer):
    end_date = serializers.SerializerMethodField()
    TA = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    velocity = serializers.SerializerMethodField()
    total_goal = serializers.SerializerMethodField()
    generated = serializers.SerializerMethodField()
    generated_pos = serializers.SerializerMethodField()
    sections = SectionsSettingsSerializer(read_only=True, many=True)
    #tactics = TacticsSerializer(read_only=True, many=True)
    tactics = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = (
            "end_date", "TA", "duration", "state", "velocity", "pacing", "integration",
            "total_goal", "generated", "generated_pos", "sections", "tactics",
        )

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
    client = ClientSerializer(read_only=True, many=False)
    targets = TargetSectionSerializer(read_only=True, many=True)
    tactics = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = (
            "client", "start_date", "end_date", "name", "integration",  "pacing", "targets", "tactics"
        )

    def get_tactics(self, instance):
        model_tactics = instance.tactics.values_list('id', flat=True)
        t = Tactics.objects.all().values()
        for i in t:
            i['active'] = True if i.get('id') in model_tactics else False
        return t


class AssetsSectionSerializer(serializers.ModelSerializer):
    titles = JobTitlesSerializer(allow_null=True)

    class Meta:
        model = AssetsSection
        fields = (
            "id", "name", "landing_page",  "percent", "campaign", "titles"
        )


class IntentFeedsSectionSerializer(serializers.ModelSerializer):
    leads_generated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IntentFeedsSection
        fields = (
            "id", "name", "campaign",  "company", "leads_generated", "kind",
        )

    def get_leads_generated(self, instance):
        return instance.leads_generated


class JobTitlesSectionSerializer(serializers.ModelSerializer):
    job_title = JobTitlesSerializer(many=False)
    leads_generated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobTitlesSection
        fields = (
            "id", "job_title", "campaign",   "leads_generated",
        )

    def get_leads_generated(self, instance):
        return instance.leads_generated


class IndustriesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustriesSection
        fields = (
            "id", "name", "campaign",
        )


class RevenueSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueSection
        fields = (
            "id", "name", "campaign",
        )


class CompanySizeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySizeSection
        fields = (
            "id", "name", "campaign",
        )


class GeolocationsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeolocationsSection
        fields = (
            "id", "name", "geolocation", "campaign",
        )


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
    leads = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ABMSection
        fields = (
            "id",  "campaign", "file", "accounts", "name", "percent", "leads"
        )

    def get_leads(self, instance):
        return instance.leads


class InstallBaseSectionSerializer(serializers.ModelSerializer):
    leads_installbase = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InstallBaseSection
        fields = (
            "id",  "campaign", "name",  "leads_installbase"
        )

    def get_leads_installbase(self, instance):
        return instance.leads_installbase


class FairTradeSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FairTradeSection
        fields = (
            "id",  "campaign", "name", "value"
        )


class LeadCascadeProgramSectionSerializer(serializers.ModelSerializer):
    leads_cascade = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadCascadeProgramSection
        fields = (
            "id", "campaign", "name", "percent", 'leads_cascade'
        )

    def get_leads_cascade(self, instance):
        return instance.leads_cascade


class NurturingSectionSerializer(serializers.ModelSerializer):

    assets = AssetsSectionSerializer()
    link = serializers.SerializerMethodField(read_only=True)
    generated_leads = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NurturingSection
        fields = (
            "id", "campaign", "name", "assets", "link", "generated_leads"
        )

    def get_link(self, instance):
        return instance.link

    def get_generated_leads(self, instance):
        return instance.generated_leads


class CreativesSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreativesSection
        fields = (
            "id", "subject_line", "email_text", "landing_page", "banners"
        )


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
            "id", "title", "accounts_value"
        )


class CampaignSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    kind = serializers.CharField(default=Campaign.CampaignKinds.USER)

    assets = AssetsSectionSerializer(many=True, read_only=True)
    intents = IntentFeedsSectionSerializer(many=True, read_only=True)
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
    #start_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Campaign
        fields = (
            "id", #"client",
            "created", "active", "customer_information", "contact_name", "email", "note",
            "name", "campaign_type", "order",
            "start_date", "end_date", "kind", "dashboard_string_count",
            "state",  "details",   "guarantees", "integration", "pacing", "assets", "intents", "titles",
            "industries", "revenues", "companies_size", "geolocations", "bants", "custom_questions", "abms",
            "install_base", "fair_trades", "lead_cascades", "nurturings", "creatives"

        )

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