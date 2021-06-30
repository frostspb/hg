from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField
from django.core.validators import MaxValueValidator, MinValueValidator
from model_clone import CloneMixin
from hourglass.clients.models import Client, Company

from .base import BaseStateItem, BaseReportPercentItem

from hourglass.references.models import CampaignTypes, Geolocations, JobTitles, Tactics, Question, Managers, ITCurated

from .managers import CampaignsManager


JOB_TITLES_SLUG = "JobTitle"
ASSETS_SLUG = "Assets"
INTENT_FEED_SLUG = "IntentFeed"
ABM_SLUG = "ABM"
SUPP_LIST_SLUG = "SuppressionList"
INDUSTRIES_SLUG = "Industries"
GEO_SLUG = "Geo"
REVENUE_SLUG = "Revenue"
COMPANY_SIZE_SLUG = "CompanySize"
BANT_SLUG = "BANT"
CQ_SLUG = "CQ"
INSTALL_BASE_SLUG = "InstallBase"
CN_SLUG = "CN"
TACTICS_SLUG = "Tactics"

ITC_SLUG = "ITCurated"
FT_SLUG = "Fair-TradeLeadQualification"
LCP_SLUG = "LeadCascadeProgram'"
NURTURING_SLUG = "Nurturing"
CREATIVES_SLUG = "Creatives"

JOB_TITLES_NAME = "Job Title"
ASSETS_NAME = "Assets"
INTENT_FEED_NAME = "Intent Feed"
ABM_NAME = "ABM"
SUPP_LIST_NAME = "Suppression list(s)"
INDUSTRIES_NAME = "Industries"
GEO_NAME = "Geolocation"
REVENUE_NAME = "Revenue"
COMPANY_SIZE_NAME = "Company Size"
BANT_NAME = "BANT questions"
CQ_NAME = "Custom Questions"
INSTALL_BASE_NAME = "Install Base"
CN_NAME = "CN"
TACTICS_NAME = "Tactics"

ITC_NAME = "IT Curated"
FT_NAME = "Fair-Trade Lead Qualification"
LCP_NAME = "Lead Cascade Program'"
NURTURING_NAME = "Nurturing"
CREATIVES_NAME = "Creatives"


class Campaign(CloneMixin, BaseStateItem):
    class CampaignKinds(models.TextChoices):
        STANDARD = 'standard', 'Standard'
        USER = 'copy', 'Copy'
        CONTRACT = 'contract', 'Contract'

    class IntegrationTypes(models.TextChoices):
        SALESFORCE = 'salesforce', 'Salesforce'
        MARKETO = 'marketo', 'Marketo'
        HUB_SPOT = 'hub_spot', 'HubSpot'
        INTEGRATE = 'integrate', 'Integrate'
        LOLAGROVE = 'lolagrove', 'Lolagrove'

    class PacingTypes(models.TextChoices):
        EVEN = 'even', 'Even'
        FRONT_LOAD = 'front-load', 'Front-Load'

    # front

    contact_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField("Start Date", null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)
    order = models.IntegerField("Purchase Order", null=True)
    customer_information = models.CharField("Customer information", max_length=250, null=True, blank=True)
    details = models.TextField("Campaign Details", null=True, blank=True)
    guarantees = models.TextField("Campaign Guarantees", null=True, blank=True)
    email = models.EmailField("Email")
    note = models.TextField("Notes", null=True, blank=True)

    # both
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField("Campaign Name", max_length=250)
    campaign_type = models.CharField("Campaign Type", max_length=128, null=True, blank=True)

    # sys
    active = models.BooleanField(default=True)
    kind = models.CharField(max_length=16, choices=CampaignKinds.choices, default=CampaignKinds.STANDARD)

    # admin
    managed_by = models.ForeignKey(Managers, on_delete=models.CASCADE, null=True)
    start_offset = models.PositiveSmallIntegerField("Start Date offset in days", default=0)
    end_offset = models.PositiveSmallIntegerField("End Date offset in days", default=0)
    audience_targeted = models.IntegerField("Base Target Audience", default=0)
    integration = models.CharField(max_length=16, choices=IntegrationTypes.choices, default=IntegrationTypes.SALESFORCE)
    pacing = models.CharField(max_length=16, choices=PacingTypes.choices, default=PacingTypes.EVEN)
    tactics = models.ManyToManyField(Tactics, null=True, blank=True)
    job_titles = models.ManyToManyField(JobTitles, null=True, blank=True)
    base_velocity = models.IntegerField("Base Velocity", default=0)
    top_percent = models.FloatField("Top Leads Percent", default=0)
    middle_percent = models.FloatField("Middle Leads Percent", default=0)
    bottom_percent = models.FloatField("Bottom Leads Percent", default=0)
    dashboard_string_count = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    remaining_admin_percent = models.PositiveSmallIntegerField(default=0)
    in_progress_admin_percent = models.PositiveSmallIntegerField(default=0)

    intent_feed_goal_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    intent_feed_done_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    abm_goal_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

    objects = CampaignsManager()
    _clone_m2o_or_o2m_fields = [
        "bants", "cqs", "geolocations", "companies", "revenues", "industries",
        "intents", "titles", "assets", "targets", "sections", "creatives", "nurturings", "itcurateds",
        "lead_cascades", "ibs", "fair_trades", "abms", "sups"
    ]

    _clone_m2m_fields = ["tactics"]

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"Campaign{self.id}"

    @property
    def goal_abm(self):
        return round((self.abm_goal_percent / 100) * self.total_goal, 2)

    @property
    def done_abm(self):
        res = 0
        for abm in self.abms.all():
            res += abm.leads
        return round(res, 2)

    @property
    def done_abm_percent(self):
        if self.goal_abm:
            return round((self.done_abm/self.goal_abm) * 100, 2)
        return 0

    @property
    def total_intent_feed(self):
        res = 0
        for intent in self.intents.all():
            res += intent.leads_generated
        return round(res, 2)

    @property
    def total_intent_feed_infusemedia(self):
        res = 0
        for intent in self.intents.filter(kind=IntentFeedsSection.Kinds.INFUSEMEDIA):
            res += intent.leads_generated
        return round(res, 2)

    @property
    def total_intent_feed_bombora(self):
        res = 0
        for intent in self.intents.filter(kind=IntentFeedsSection.Kinds.BOMBORA):
            res += intent.leads_generated
        return round(res, 2)

    @property
    def total_intent_feed_aberdeen(self):
        res = 0
        for intent in self.intents.filter(kind=IntentFeedsSection.Kinds.ABERDEEN):
            res += intent.leads_generated
        return round(res, 2)

    @property
    def goal_intent_feed(self):
        return round((self.intent_feed_goal_percent / 100) * self.total_goal, 2)

    @property
    def done_intent_feed(self):
        return round((self.intent_feed_done_percent / 100) * self.goal_intent_feed, 2)

    @property
    def total_goal(self):
        res = self.targets.filter().aggregate(Sum('leads_goal')).get('leads_goal__sum', 0)
        if not res:
            res = 0
        return round(res,2)

    @property
    def total_generated(self):
        res = self.targets.filter().aggregate(Sum('leads_generated')).get('leads_generated__sum', 0)
        if not res:
            res = 0
        return res

    @property
    def initial_start_date(self):
        return now() - timedelta(days=self.start_offset)

    @property
    def velocity(self):
        sections = self.sections.filter(enabled=True)
        sections_v = self.sections.filter(enabled=True).aggregate(Sum('delta_v_sector'))
        _velocity = self.base_velocity + sections_v.get('delta_v_sector__sum', 0)
        for i in sections:
            if i.name == ASSETS_SLUG:
                _velocity += self.assets.count() * i.delta_v_per_row
            elif i.name == BANT_SLUG:
                _velocity += self.bants.count() * i.delta_v_per_row
            elif i.name == CQ_SLUG:
                _velocity += self.cqs.count() * i.delta_v_per_row
        targets_velocity = self.targets.filter(state=BaseStateItem.States.STATE_RUNNING).aggregate(Sum('velocity'))

        if targets_velocity:
            tv = targets_velocity.get('velocity__sum', 0)
            if tv:
                _velocity += tv
        return _velocity

    @property
    def delivered(self):
        if self.total_goal:
            return int((self.total_generated/self.total_goal) * 100)

    @property
    def remaining(self):
        if self.total_goal:
            return int(((self.total_goal - self.total_generated) / self.total_goal) * self.remaining_admin_percent)

    @property
    def in_validation(self):
        if self.total_goal:
            return int(((self.total_goal - self.total_generated) / self.total_goal) * self.in_progress_admin_percent)

    @property
    def generated(self):
        res = self.velocity * self.duration
        if res >= self.total_goal:
            res = self.total_goal
        return res

    @property
    def generated_pos(self):
        return {
            'top': self.generated * self.top_percent,
            'middle': self.generated * self.middle_percent,
            'bottom': self.generated * self.bottom_percent,
        }

    @property
    def ta(self):
        sections = self.sections.filter(enabled=True)
        sections_ta = self.sections.filter(enabled=True).aggregate(Sum('delta_ta_sector'))

        # sections_velocity = self.sections.filter(enabled=True).aggregate(Sum('delta_v'))
        ta = self.audience_targeted + sections_ta.get('delta_ta_sector__sum', 0)

        for i in sections:
            if i.name == JOB_TITLES_SLUG:
                ta += self.titles.count() * i.delta_ta_per_row
            elif i.name == REVENUE_SLUG:
                ta += self.revenues.count() * i.delta_ta_per_row
            elif i.name == COMPANY_SIZE_SLUG:
                ta += self.companies.count() * i.delta_ta_per_row
            elif i.name == SUPP_LIST_SLUG:
                pass
            elif i.name == ABM_SLUG:
                #abm_ta = self.abm
                pass
            elif i.name == INDUSTRIES_SLUG:
                ta += self.industries.count() * i.delta_ta_per_row
        return ta

    @property
    def initial_end_date(self):
        return now() + timedelta(days=self.end_offset)

    @property
    def is_standard(self):
        return self.kind == self.CampaignKinds.STANDARD


class SectionSettings(CloneMixin, models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField("Section", max_length=64)
    slug = models.SlugField(max_length=64)
    enabled = models.BooleanField(default=True)
    can_enabled = models.BooleanField(default=True)
    delta_ta_sector = models.IntegerField("% Change of TA by Sector", default=0)
    delta_ta_per_row = models.IntegerField("% Change of TA by Each Line", default=0)
    delta_v_sector = models.IntegerField("Speed Change by Sector", default=0)
    delta_v_per_row = models.IntegerField("Speed Change by Each Line", default=0)
    quality_sector = models.IntegerField("Change of Quality by Sector", default=0)
    quality_per_row = models.IntegerField("Change of Quality by Each Line", default=0)

    class Meta:
        verbose_name = "Section Settings"
        verbose_name_plural = "Section Settings"

    def __str__(self):
        return f"Section {self.name}"


class TargetSection(CloneMixin, BaseStateItem):
    campaign_pos_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE)
    leads_goal = models.PositiveIntegerField('Leads goal', default=0)
    leads_generated = models.PositiveIntegerField('Leads Generated', default=0)
    velocity = models.PositiveSmallIntegerField("Velocity", default=0)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="targets")

    @property
    def remaining_leads(self):
        return self.leads_goal - self.leads_generated

    @property
    def percent_completion(self):
        if self.leads_goal > 0:
            return int((self.leads_generated / self.leads_goal) * 100)

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaign"

    def __str__(self):
        return f"#{self.id}"

    # @property
    # def execution_time


class AssetsSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Asset Name", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="assets")
    landing_page = models.FileField("Landing Page")
    titles = models.ManyToManyField(JobTitles, blank=True)
    velocity_koeff = models.FloatField(default=1.0)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"#{self.id}"

    @property
    def leads_assets(self):
        return (self.percent / 100) * self.campaign.total_generated


class IntentFeedsSection(CloneMixin, BaseReportPercentItem):
    class Kinds(models.TextChoices):
        INFUSEMEDIA = 'INFUSEmedia', 'INFUSEmedia'
        BOMBORA = 'Bombora', 'Bombora'
        ABERDEEN = 'Aberdeen', 'Aberdeen'

    name = models.CharField("Intent topic", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="intents")
    company = models.ManyToManyField(Company, null=True, blank=True, verbose_name="Companies")
    kind = models.CharField(" Integration Platform", max_length=32, choices=Kinds.choices, default=Kinds.INFUSEMEDIA)
    companies_count = models.PositiveSmallIntegerField("Companies Generated", default=0)

    class Meta:
        verbose_name = "Intent Feed"
        verbose_name_plural = "Intent Feeds"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_generated(self):
        return (self.percent/100 ) * self.campaign.done_intent_feed

    @property
    def goal_intent_feed(self):
        return (self.percent / 100) * self.campaign.total_goal


class JobTitlesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Name", max_length=200, null=True, blank=True)
    job_title = models.ForeignKey(JobTitles, on_delete=models.CASCADE, verbose_name="Title Captured")
    generated = models.PositiveSmallIntegerField("Leads Generated", default=0)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="titles")
    goal = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_generated(self):
        return (self.generated / 100) * self.campaign.total_goal


class SuppresionListSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="sups")
    title = models.CharField(max_length=128)
    accounts_value = models.PositiveSmallIntegerField()


class IndustriesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Industry", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="industries")

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_industry(self):
        return (self.percent / 100) * self.campaign.total_goal


class GeolocationsSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Geolocation title", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="geolocations")
    geolocation = models.ForeignKey(Geolocations, on_delete=models.CASCADE)
    goal_per_geo = models.FloatField("Goal per Geo", default=0)

    class Meta:
        verbose_name = "Geolocation"
        verbose_name_plural = "Geolocations"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_geolocation(self):
        return (self.percent / 100) * self.campaign.total_goal


class RevenueSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Revenue", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="revenues")

    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenue"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_revenue(self):
        return (self.percent / 100) * self.campaign.total_goal


class CompanySizeSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Company Size", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="companies")

    class Meta:
        verbose_name = "Company Size"
        verbose_name_plural = "Companies Sizes"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_company_size(self):
        return (self.percent / 100) * self.campaign.total_goal


class BANTQuestionsSection(CloneMixin, models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="bants")
    answer = models.TextField("Answer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "BANT Question"
        verbose_name_plural = "BANT Questions"

    def __str__(self):
        return f"{self.id}"


class CustomQuestionsSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="cqs")
    answer = models.TextField("Answer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Custom Question"
        verbose_name_plural = "Custom Questions"

    def __str__(self):
        return f"{self.id}"


class ABMSection(CloneMixin, BaseReportPercentItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="abms")
    file = models.FileField("List")
    accounts = models.IntegerField("Accounts", default=0)
    name = models.CharField(max_length=256, null=True)

    class Meta:
        verbose_name = "ABM"
        verbose_name_plural = "ABM"

    @property
    def leads(self):
        return (self.percent/100) * self.campaign.total_goal


class FairTradeSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="fair_trades")
    name = models.CharField("Treat Desctiption", max_length=256)
    value = models.CharField("Value", max_length=256)


class InstallBaseSection(CloneMixin, BaseReportPercentItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="ibs")
    name = models.CharField("Title", max_length=256)

    @property
    def leads_installbase (self):
        return (self.percent / 100) * self.campaign.total_generated


class LeadCascadeProgramSection(CloneMixin, BaseReportPercentItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="lead_cascades")
    name = models.CharField("Leads Description", max_length=256)

    @property
    def leads_cascade (self):
        return (self.percent / 100) * self.campaign.total_generated


class NurturingSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="nurturings")
    name = models.CharField("Type", max_length=256)
    assets = models.ForeignKey(AssetsSection, on_delete=models.CASCADE)

    @property
    def link(self):
        return self.assets.landing_page

    @property
    def generated_leads(self):
        return self.assets.leads_assets


class CreativesSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="creatives")
    name = models.EmailField("email")
    value = models.TextField()


class ITCuratedSection(CloneMixin, models.Model):
    class Statuses(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSE = 'pause', 'Pause'
        REQUESTED = 'requested', 'Requested'

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="itcurateds")
    status = models.CharField(max_length=16, choices=Statuses.choices, default=Statuses.ACTIVE)
    curated = models.ForeignKey(ITCurated, related_name='curateds', on_delete=models.CASCADE)
    pos = models.SmallIntegerField('Position', default=0)


@receiver(post_save, sender=Campaign)
def create_settings(sender, instance, created, **kwargs):

    sections = [

        {'name': ASSETS_NAME, 'slug': ASSETS_SLUG},
        {'name': INTENT_FEED_NAME, 'slug': INTENT_FEED_SLUG},
        {'name': ABM_NAME, 'slug': ABM_SLUG},
        {'name': SUPP_LIST_NAME, 'slug': SUPP_LIST_SLUG},
        {'name': JOB_TITLES_NAME, 'slug': JOB_TITLES_SLUG},
        {'name': INDUSTRIES_NAME, 'slug': INDUSTRIES_SLUG},
        {'name': GEO_NAME, 'slug': GEO_SLUG},
        {'name': REVENUE_NAME, 'slug': REVENUE_SLUG},
        {'name': COMPANY_SIZE_NAME, 'slug': COMPANY_SIZE_SLUG},
        {'name': BANT_NAME, 'slug': BANT_SLUG},
        {'name': CQ_NAME, 'slug': CQ_SLUG},
        {'name': INSTALL_BASE_NAME, 'slug': INSTALL_BASE_SLUG},
        #{'name': CN_NAME, 'slug': CN_SLUG},
        #{'name': TACTICS_NAME, 'slug': TACTICS_SLUG},
        {'name': ITC_NAME, 'slug': ITC_SLUG},
        {'name': FT_NAME, 'slug': FT_SLUG},
        {'name': LCP_NAME, 'slug': LCP_SLUG},
        {'name': NURTURING_NAME, 'slug': NURTURING_SLUG},
        {'name': CREATIVES_NAME, 'slug': CREATIVES_SLUG},
    ]

    if created:
        for_create = [SectionSettings(slug=i.get('slug'), campaign=instance, name=i.get('name')) for i in sections]
        SectionSettings.objects.bulk_create(for_create)
