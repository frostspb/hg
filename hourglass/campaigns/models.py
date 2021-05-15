from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField
from model_clone import CloneMixin
from hourglass.clients.models import Client

from .base import BaseStateItem, BaseReportPercentItem

from hourglass.references.models import CampaignTypes, Geolocations, JobTitles

from .managers import CampaignsManager


JOB_TITLES = "JobTitle"
ASSETS = "Assets"
INTENT_FEED = "IntentFeed"
ABM = "ABM"
SUPP_LIST = "SuppressionList"
INDUSTRIES = "Industries"
GEO = "Geo"
REVENUE = "Revenue"
COMPANY_SIZE = "CompanySize"
BANT = "BANT"
CQ = "CQ"
INSTALL_BASE = "InstallBase"
CN = "CN"
TACTICS = "Tactics"


class Campaign(CloneMixin, BaseStateItem):
    class CampaignKinds(models.TextChoices):
        STANDARD = 'standard', 'Standard'
        USER = 'copy', 'Copy'
        CONTRACT = 'contract', 'Contract'

    customer_information = models.CharField("Customer information", max_length=250)
    contact_name = models.CharField("Contact Name", max_length=250)
    email = models.EmailField("Email")
    note = models.TextField("Notes", null=True, blank=True)
    name = models.CharField("Campaign Name", max_length=250)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    start_offset = models.PositiveSmallIntegerField("Start Date offset in days", default=0)
    end_offset = models.PositiveSmallIntegerField("End Date offset in days", default=0)
    audience_targeted = models.IntegerField("Base Target Audience", default=0)
    kind = models.CharField(max_length=16, choices=CampaignKinds.choices, default=CampaignKinds.STANDARD)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    order = models.IntegerField("Purchase Order", null=True)
    campaign_type = models.CharField("Campaign Type", max_length=128, null=True, blank=True)
    details = models.TextField("Campaign Details", null=True, blank=True)
    guarantees = models.TextField("Campaign Guarantees", null=True, blank=True)
    base_velocity = models.IntegerField("Base Velocity", default=0)
    top_percent = models.FloatField("Top Leads Percent", default=0)
    middle_percent = models.FloatField("Middle Leads Percent", default=0)
    bottom_percent = models.FloatField("Bottom Leads Percent", default=0)

    objects = CampaignsManager()
    _clone_m2o_or_o2m_fields = [
        "bants", "cqs", "geolocations", "companies", "revenues", "industries",
        "intents", "titles", "assets", "targets", "sections",
    ]

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"Campaign{self.id}"

    @property
    def total_goal(self):
        res = self.targets.filter().aggregate(Sum('leads_goal')).get('leads_goal__sum', 0)
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
            if i.name == ASSETS:
                _velocity += self.assets.count() * i.delta_v_per_row
            elif i.name == BANT:
                _velocity += self.bants.count() * i.delta_v_per_row
            elif i.name == CQ:
                _velocity += self.cqs.count() * i.delta_v_per_row
        targets_velocity = self.targets.filter(state=BaseStateItem.States.STATE_RUNNING).aggregate(Sum('velocity'))

        if targets_velocity:
            tv = targets_velocity.get('velocity__sum', 0)
            if tv:
                _velocity += tv
        return _velocity

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
            if i.name == JOB_TITLES:
                ta += self.titles.count() * i.delta_ta_per_row
            elif i.name == REVENUE:
                ta += self.revenues.count() * i.delta_ta_per_row
            elif i.name == COMPANY_SIZE:
                ta += self.companies.count() * i.delta_ta_per_row
            elif i.name == SUPP_LIST:
                pass
            elif i.name == ABM:
                #abm_ta = self.abm
                pass
            elif i.name == INDUSTRIES:
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
    name = models.CharField("Section", max_length=32)
    enabled = models.BooleanField(default=True)
    can_enabled = models.BooleanField(default=True)
    delta_ta_sector = models.IntegerField(default=0)
    delta_ta_per_row = models.IntegerField(default=0)
    delta_v_sector = models.IntegerField(default=0)
    delta_v_per_row = models.IntegerField(default=0)

    def __str__(self):
        return f"Section {self.name}"


class TargetSection(CloneMixin, BaseStateItem):
    class IntegrationTypes(models.TextChoices):
        SALESFORCE = 'salesforce', 'Salesforce'
        MARKETO = 'marketo', 'Marketo'
        HUB_SPOT = 'hub_spot', 'HubSpot'
        INTEGRATE = 'integrate', 'Integrate'
        LOLAGROVE = 'lolagrove', 'Lolagrove'

    class PacingTypes(models.TextChoices):
        EVEN = 'even', 'Even'
        FRONT_LOAD = 'front-load', 'Front-Load'

    integration = models.CharField(max_length=16, choices=IntegrationTypes.choices, default=IntegrationTypes.SALESFORCE)
    pacing = models.CharField(max_length=16, choices=PacingTypes.choices, default=PacingTypes.EVEN)
    leads_goal = models.PositiveIntegerField('Leads goal')
    leads_generated = models.PositiveIntegerField('Leads Generated', default=0)
    velocity = models.PositiveSmallIntegerField("Velocity", default=0)
    campaign_pos_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="targets")

    @property
    def remaining_leads(self):
        return self.leads_goal - self.leads_generated

    @property
    def percent_completion(self):
        return int((self.leads_generated / self.leads_goal) * 100)

    def __str__(self):
        return f"{self.id}"

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
        return f"{self.id}"


class IntentFeedsSection(CloneMixin,BaseReportPercentItem):
    name = models.CharField("Intent topic", max_length=200)
    generated = models.PositiveSmallIntegerField("Leads Generated", default=0)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="intents")

    class Meta:
        verbose_name = "Intent Feed"
        verbose_name_plural = "Intent Feeds"

    def __str__(self):
        return f"{self.id}"


class JobTitlesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Job Titles", max_length=200)
    generated = models.PositiveSmallIntegerField("Leads Generated", default=0)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="titles")

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

    def __str__(self):
        return f"{self.id}"


class IndustriesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Industry", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="industries")

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return f"{self.id}"


class RevenueSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Revenue", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="revenues")

    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenue"

    def __str__(self):
        return f"{self.id}"


class CompanySizeSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Company Size", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="companies")

    class Meta:
        verbose_name = "Company Size"
        verbose_name_plural = "Companies Sizes"

    def __str__(self):
        return f"{self.id}"


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


class BANTQuestionsSection(CloneMixin, models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="bants")
    answer = models.TextField("Answer")


class CustomQuestionsSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="cqs")
    answer = models.TextField("Answer")


@receiver(post_save, sender=Campaign)
def create_settings(sender, instance, created, **kwargs):

    sections = [
        JOB_TITLES,
        ASSETS,
        INTENT_FEED,
        ABM,
        SUPP_LIST,
        INDUSTRIES,
        GEO,
        REVENUE,
        COMPANY_SIZE,
        BANT,
        CQ,
        INSTALL_BASE,
        CN,
        TACTICS,
    ]
    
    if created:
        for_create = [SectionSettings(name=i, campaign=instance) for i in sections]
        SectionSettings.objects.bulk_create(for_create)
