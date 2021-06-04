from django.db import models

from django_extensions.db.models import TimeStampedModel


class Client(TimeStampedModel):
    class ClientTypes(models.TextChoices):
        STANDARD = 'standard', 'Standard client'
        PROSPECTIVE = 'prospective', 'Prospective client'
        CONTRACT = 'contract', 'Contract client'

    name = models.CharField(max_length=50, unique=True)
    client_type = models.CharField(max_length=16, choices=ClientTypes.choices, default=ClientTypes.STANDARD)
    total_campaigns = models.IntegerField("Total Campaigns", default=0)
    leads_generated = models.IntegerField("Leads Generated Totally", default=0)
    client_since = models.DateField("Our Client since", null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    @property
    def current_campaigns(self):
        return self.campaign_set.all().count()

    @property
    def current_leads_goals(self):
        s = 0
        for i in self.campaign_set.all():
            s += i.total_goal
        return s

    def __str__(self):
        return f"{self.name}"


class Company(TimeStampedModel):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

