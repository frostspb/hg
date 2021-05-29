from datetime import timedelta
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField


class CampaignTypes(models.Model):
    name = models.CharField("Type", max_length=64)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Campaign Type"
        verbose_name_plural = "Campaigns Types"

    def __str__(self):
        return self.name


class Geolocations(models.Model):
    name = models.CharField("Geolocation", max_length=64)

    class Meta:
        verbose_name = "Geolocation"
        verbose_name_plural = "Geolocations"

    def __str__(self):
        return self.name


class JobTitles(models.Model):
    name = models.CharField("Job Title", max_length=128)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "JobTitle"

    def __str__(self):
        return self.name


class Tactics(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Tactic"
        verbose_name_plural = "Tactics"

    def __str__(self):
        return self.name


class Answers(models.Model):
    value = models.TextField()

class Question(models.Model):
    class QuestionKinds(models.TextChoices):
        BANT = 'BANT', 'BANT'
        CUSTOM = 'custom', 'Custom'

    kind = models.CharField(max_length=16, choices=QuestionKinds.choices, default=QuestionKinds.BANT)
    name = models.TextField()
    answer_variants = models.ManyToManyField(Answers)