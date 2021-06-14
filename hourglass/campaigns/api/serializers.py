from rest_framework import serializers

from ..models import Campaign, TargetSection, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection,ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection
from hourglass.references.models import CampaignTypes, Tactics, JobTitles, Geolocations
from hourglass.references.api.serializers import AnswerSerializer, QuestionSerializer, JobTitlesSerializer, ITCuratedSerializer
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


class CampaignSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    kind = serializers.CharField(default=Campaign.CampaignKinds.USER)
    #pos = CampaignsSectionSerializer(source='campaignpos_set', many=True)

    #start_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Campaign
        fields = (
            "id", "client", "created", "active", "customer_information", "contact_name", "email", "note",
            "name", "campaign_type", "order",
            "start_date", "end_date", "kind", "state",  "details",   "guarantees", "integration", "pacing"
        )

    def get_start_date(self, instance):
        if instance.is_standard:
            return instance.initial_start_date
        return instance.start_date

    def get_end_date(self, instance):
        if instance.is_standard:
            return instance.initial_end_date
        return instance.end_date


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
        if instance.end_date:
            return instance.end_date.strftime('%d-%m-%Y')

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
    class Meta:
        model = IntentFeedsSection
        fields = (
            "id", "name", "campaign",  "company", "generated", "kind",
        )


class JobTitlesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitlesSection
        fields = (
            "id", "name", "campaign",   "generated",
        )


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
    question = QuestionSerializer()

    class Meta:
        model = BANTQuestionsSection
        fields = (
            "id", "campaign", "question", "answer"
        )


class CustomQuestionsSectionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = CustomQuestionsSection
        fields = (
            "id",  "campaign", "question", "answer"
        )


class ABMSectionSerializer(serializers.ModelSerializer):
    goal_abm = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ABMSection
        fields = (
            "id",  "campaign", "file", "accounts", "name", "percent", "goal_abm"
        )

    def get_goal_abm(self, instance):
        return instance.goal_abm


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
            "id", "campaign", "name", "percent"
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
            "id", "name", "value",
        )


class ITCuratedSectionSerializer(serializers.ModelSerializer):
    curated = ITCuratedSerializer()

    class Meta:
        model = ITCuratedSection
        fields = (
            "id", "curated", "status", "pos"
        )