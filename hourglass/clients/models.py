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
    client_since = models.DateTimeField("Our Client since", null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name}"
