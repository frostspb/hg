from datetime import timedelta
from django.db import models

from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel

from hourglass.clients.models import Client


class CampaignTypes(models.Model):
    name = models.CharField("Type", max_length=64)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Campaign Type"
        verbose_name_plural = "Campaigns Types"

    def __str__(self):
        return self.name


class CampaignBase(TimeStampedModel):
    name = models.CharField("Name", max_length=64)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    start_offset = models.PositiveSmallIntegerField("Start Date offset in days")
    end_offset = models.PositiveSmallIntegerField("End Date offset in days")
    audience_targeted = models.IntegerField("Audience Targeted")

    class Meta:
        abstract = True

    @property
    def start_date(self):
        return now() - timedelta(days=self.start_offset)

    @property
    def end_date(self):
        return now() + timedelta(days=self.end_offset)


class CampaignTemplate(CampaignBase):

    class Meta:
        verbose_name = "Campaign Template"
        verbose_name_plural = "Campaigns Templates"

    def __str__(self):
        return f"Template{self.id}"


class CampaignStandard(CampaignBase):
    template = models.ForeignKey(CampaignTemplate, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"Campaign{self.id}"


class CampaignPosBase(models.Model):
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
    campaign_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @property
    def remaining_leads(self):
        return self.leads_goal - self.leads_generated

    @property
    def percent_completion(self):
        return int((self.leads_generated / self.leads_goal) * 100)

    def __str__(self):
        return f"{self.id}"


class CampaignTemplatePos(CampaignPosBase):
    campaign = models.ForeignKey(CampaignTemplate, on_delete=models.CASCADE)


class CampaignPos(CampaignPosBase):
    campaign = models.ForeignKey(CampaignStandard, on_delete=models.CASCADE)
