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
    code = models.CharField("Code", max_length=16, null=True, blank=True)

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
        verbose_name_plural = "Job Titles"

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField("Industry", max_length=128)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industry"

    def __str__(self):
        return self.name


class CompanySize(models.Model):
    name = models.CharField("Company Size", max_length=128)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Company Size"
        verbose_name_plural = "Company Size"

    def __str__(self):
        return self.name


class Revenue(models.Model):
    name = models.CharField("Revenue", max_length=128)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenue"

    def __str__(self):
        return self.name


class Tactics(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Tactic"
        verbose_name_plural = "Tactics"

    def __str__(self):
        return self.name


class BANTQuestion(models.Model):
    class SectionKind(models.TextChoices):
        BUDGET = 'budget', 'Budget'
        AUTHORITY = 'authority', 'Authority'
        NEED = 'need', 'Need'
        TIME = 'time', 'Time'

    question = models.TextField()
    kind = models.CharField(max_length=16, choices=SectionKind.choices, default=SectionKind.BUDGET)

    def __str__(self):
        return self.question


class BANTAnswer(models.Model):

    question = models.ForeignKey(BANTQuestion, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    preferred = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class CustomQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question


class CustomAnswer(models.Model):

    question = models.ForeignKey(CustomQuestion, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    preferred = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Managers(models.Model):
    name = models.CharField(max_length=255)
    photo = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url

    def __str__(self):
        return self.name


class ITCurated(models.Model):
    slug = models.SlugField()
    visible = models.BooleanField(default=True)
    link = models.URLField("Link")
    title = models.CharField(max_length=64)

    class Meta:
        verbose_name = "IT Curated block"
        verbose_name_plural = "IT Curated blocks"


class IntegrationType(models.Model):
    name = models.CharField(max_length=250)
    image = models.FileField(null=True, blank=True)
    image_popup = models.FileField(null=True, blank=True)
