from datetime import timedelta
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField
from model_clone import CloneMixin
from hourglass.clients.models import Client

from .base import BaseStateItem, BaseReportPercentItem

from hourglass.references.models import CampaignTypes, Geolocations, JobTitles

from .managers import  CampaignsManager


def campaign_default_settings():
    return {
        "title": True,
        "assets": True,
        "intent": True,
        "abm": True,
        "suppression": True,
        "job_titles": True,
        "industries": True,
        "geo": True,
        "revenue": True,
        "company_size": True,
        "bant": True,
        "cq": True,
        "install_base": True,
        "cn": True,
        "tactics": True,
    }


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
    start_offset = models.PositiveSmallIntegerField("Start Date offset in days")
    end_offset = models.PositiveSmallIntegerField("End Date offset in days")
    audience_targeted = models.IntegerField("Audience Targeted")
    kind = models.CharField(max_length=16, choices=CampaignKinds.choices, default=CampaignKinds.STANDARD)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    settings = JSONField(null=True, verbose_name='JSON settings', default=campaign_default_settings)

    objects = CampaignsManager()
    _clone_m2o_or_o2m_fields = ["bants", "cqs", "geolocations", "companies", "revenues", "industries",
    "intents", "titles", "assets", "campaigns",]
    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"Campaign{self.id}"

    @property
    def initial_start_date(self):
        return now() - timedelta(days=self.start_offset)

    @property
    def initial_end_date(self):
        return now() + timedelta(days=self.end_offset)


class CampaignsSection(CloneMixin, BaseStateItem):
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
    leads_generated = models.PositiveIntegerField('Leads Generated')
    velocity = models.PositiveSmallIntegerField("Velocity")
    campaign_pos_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="campaigns")

    @property
    def remaining_leads(self):
        return self.leads_goal - self.leads_generated

    @property
    def percent_completion(self):
        return int((self.leads_generated / self.leads_goal) * 100)

    def __str__(self):
        return f"{self.id}"


class AssetsSection(CloneMixin,BaseReportPercentItem):
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






