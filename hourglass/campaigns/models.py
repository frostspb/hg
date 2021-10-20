from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField
import math
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from model_clone import CloneMixin
from hourglass.clients.models import Client, Company

from .base import BaseStateItem, BaseReportPercentItem

from hourglass.references.models import CampaignTypes, Geolocations, JobTitles, Tactics, Managers, ITCurated,\
    Industry, Revenue, CompanySize, Pacing, CompanyRef, NurturingStages, PartOfMap

from .managers import CampaignsManager

from smart_selects.db_fields import ChainedForeignKey
from hourglass.references.models import BANTQuestion, BANTAnswer, CustomAnswer, CustomQuestion, IntegrationType,\
    Associates

User = get_user_model()

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
LCP_SLUG = "LeadCascadeProgram"
NURTURING_SLUG = "Nurturing"
CREATIVES_SLUG = "Creatives"

JOB_TITLES_NAME = "Job Titles"
ASSETS_NAME = "Assets"
INTENT_FEED_NAME = "Data Signal Streams"
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
TACTICS_NAME = "Tactics Activated"

ITC_NAME = "IT Curated"
FT_NAME = "Fair-Trade Lead Qualification"
LCP_NAME = "Lead Cascade Program"
NURTURING_NAME = "Nurturing"
CREATIVES_NAME = "Creatives"


def format_leads(percent, value):
    return int(round((percent / 100) * value, 0))


class Campaign(CloneMixin, BaseStateItem):
    class CampaignKinds(models.TextChoices):
        STANDARD = 'standard', 'Standard'
        USER = 'copy', 'Copy'
        CONTRACT = 'contract', 'Contract'

    # front

    contact_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField("Start Date", null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)
    order = models.IntegerField("Purchase Order", null=True, blank=True)
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
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    # admin
    managed_by = models.ForeignKey(Managers, on_delete=models.CASCADE, null=True)
    start_offset = models.PositiveIntegerField("Start Date offset in days", default=0)
    end_offset = models.PositiveIntegerField("End Date offset in days", default=0)
    audience_targeted = models.IntegerField("Base Target Audience", default=0)
    integration_type = models.ForeignKey(
        IntegrationType, on_delete=models.CASCADE, verbose_name="Integration", blank=True, null=True)

    pending = models.PositiveIntegerField("Pending in Integration", blank=True, null=True)

    pacing_type = models.ForeignKey(
        Pacing, on_delete=models.CASCADE, verbose_name="Pacing" , blank=True, null=True)
    tactics = models.ManyToManyField(Tactics, null=True, blank=True)
    job_titles = models.ManyToManyField(JobTitles, null=True, blank=True,
                                        verbose_name="Titles generated by Artificial Intelligence", related_name="jt")
    base_velocity = models.IntegerField("Leads Generated per Minute Speed", default=0)
    base_quality = models.IntegerField(default=0)
    top_percent = models.FloatField("Top Leads Percent", null=True, blank=True)
    middle_percent = models.FloatField("Middle Leads Percent",  null=True, blank=True)
    bottom_percent = models.FloatField("Bottom Leads Percent", null=True, blank=True)
    dashboard_string_count = models.PositiveIntegerField(
        "Lead Goal Lower Lines (Dashboard View)",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    ta_volume = models.PositiveIntegerField(
        "Target Audience Volume (in cubes)",
        default=0,

    )
    maximum_campaign_completeness = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], null=True, blank=True
    )
    engagement_in_process = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], null=True, blank=True
    )
    remaining_admin_percent = models.PositiveIntegerField(default=0)

    in_progress_admin_percent = models.PositiveIntegerField(default=0)

    intent_feed_goal_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    intent_feed_done_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    abm_look_a_like = models.PositiveIntegerField("Look-a-like", blank=True, null=True)
    abm_look_a_like_state = models.CharField("Look-a-like state",
        max_length=16, choices=BaseStateItem.States.STATE_CHOICES, default=BaseStateItem.States.STATE_RUNNING
    )
    abm_goal_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    nurturing_parameters = models.CharField(max_length=250, null=True, blank=True)
    part_of_the_map = models.ForeignKey(PartOfMap,  null=True, blank=True, on_delete=models.CASCADE)
    objects = CampaignsManager()
    _clone_m2o_or_o2m_fields = [
        "bants", "cqs", "geolocations", "companies", "revenues", "industries",
        "intents", "titles", "assets", "targets",  "creatives", "nurturings", #  "itcurateds",
        "lead_cascades", "ibs", "fair_trades", "abms", "sups", "teams",
    ]

    _clone_m2m_fields = ["tactics", "jt"]

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"Campaign{self.id}"

    @property
    def engagement_in_process_value(self):
        if self.engagement_in_process and self.audience_targeted:
            return (self.engagement_in_process/100) * self.audience_targeted

    @property
    def goal_abm(self):
        return format_leads(self.abm_goal_percent, self.total_goal)

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
    def rejected(self):
        # res = self.teams.filter().aggregate(Sum('rejected')).get('rejected__sum', 0)
        # if not res:
        #     res = 0
        # return res
        res = 0
        for team in self.teams.all():
            res += team.rejected
        return int(round(res, 2))

    @property
    def total_goal(self):
        res = self.targets.filter().aggregate(Sum('leads_generated')).get('leads_generated__sum', 0)
        if not res:
            res = 0
        return int(math.floor(res))

    @property
    def total_generated_goal(self):
        res = self.targets.filter().aggregate(Sum('leads_goal')).get('leads_goal__sum', 0)
        if not res:
            res = 0
        return int(round(res, 2))

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
        #sections = self.sections.filter(enabled=True)
        sections_v = self.sections.filter(enabled=True).aggregate(Sum('delta_v_sector'))
        _velocity = self.base_velocity + sections_v.get('delta_v_sector__sum', 0)
        # for i in sections:
        #     if i.name == ASSETS_SLUG:
        #         _velocity += self.assets.count() * i.delta_v_per_row
        #     elif i.name == BANT_SLUG:
        #         _velocity += self.bants.count() * i.delta_v_per_row
        #     elif i.name == CQ_SLUG:
        #         _velocity += self.cqs.count() * i.delta_v_per_row
        targets_velocity = self.targets.filter(state=BaseStateItem.States.STATE_RUNNING).aggregate(Sum('velocity'))

        if targets_velocity:
            tv = targets_velocity.get('velocity__sum', 0)
            if tv:
                _velocity += tv
        return _velocity

    @property
    def delivered(self):
        if self.total_goal:
            return int(round((self.total_generated/self.total_goal) * 100, 0))

    @property
    def remaining(self):
        if self.total_goal:
            return int(((self.total_goal - self.total_generated) / self.total_goal) * self.remaining_admin_percent)

    @property
    def in_validation(self):
        if self.total_goal:
            return int(((self.total_goal - self.total_generated) / self.total_goal) * self.in_progress_admin_percent)

    @property
    def generated_leads(self):
        if self.delivered:
            return int(self.delivered + self.rejected)
        else:
            return 0

    @property
    def duration(self):
        if self.velocity:
            return int((self.total_generated_goal - self.total_goal) / self.velocity)
                    # if self.state == self.States.STATE_RUNNING and self.started_at:
        #     return self.execution_time + int((now() - self.started_at).total_seconds() / 60) % 60
        # else:
        #     return self.execution_time

    @property
    def generated(self):
        res = self.velocity * self.duration
        if res >= self.total_generated_goal:
            res = self.total_generated_goal
        return res

    @property
    def generated_pos(self):
        top_percent = 0 if not self.top_percent else self.top_percent
        middle_percent = 0 if not self.middle_percent else self.middle_percent
        bottom_percent = 0 if not self.bottom_percent else self.bottom_percent

        return {
            'top_value': self.generated * top_percent/100,
            'middle_value': self.generated * middle_percent/100,
            'bottom_value': self.generated * bottom_percent/100,
            'top': self.top_percent,
            'middle': self.middle_percent,
            'bottom': self.bottom_percent,
        }

    @property
    def ta(self):
        sections = self.sections.filter(enabled=True)
        sections_ta = self.sections.filter(enabled=True).aggregate(Sum('delta_ta_sector'))

        # sections_velocity = self.sections.filter(enabled=True).aggregate(Sum('delta_v'))
        ta = self.audience_targeted + sections_ta.get('delta_ta_sector__sum', 0)

        for i in sections:
            if i.name == JOB_TITLES_SLUG:
                ta += self.titles.count() * i.delta_ta_per_row_value
            elif i.name == REVENUE_SLUG:
                ta += self.revenues.count() * i.delta_ta_per_row_value
            elif i.name == COMPANY_SIZE_SLUG:
                ta += self.companies.count() * i.delta_ta_per_row_value
            elif i.name == SUPP_LIST_SLUG:
                pass
            elif i.name == ABM_SLUG:
                #abm_ta = self.abm
                pass
            elif i.name == INDUSTRIES_SLUG:
                ta += self.industries.count() * i.delta_ta_per_row_value
        return ta

    @property
    def initial_end_date(self):
        return now() + timedelta(days=self.end_offset)

    @property
    def is_standard(self):
        return self.kind == self.CampaignKinds.STANDARD

    def reset_settings(self):
        self.sections.all().delete()
        for_create = [
            SectionSettings(
                slug=i.get('slug'),
                campaign=self,
                name=i.get('name'),
                delta_v_sector=i.get('delta_v_sector', 0),
                delta_v_per_row=i.get('delta_v_per_row', 0),
                delta_ta_sector=i.get('delta_ta_sector', 0),
                delta_ta_per_row=i.get('delta_ta_per_row', 0),
                quality_sector=i.get('quality_sector'),
                quality_per_row=i.get('quality_per_row'),
            ) for i in sections
        ]
        SectionSettings.objects.bulk_create(for_create)


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
    quality_sector = models.IntegerField("Change of Quality by Sector", null=True, blank=True)
    quality_per_row = models.IntegerField("Change of Quality by Each Line", null=True, blank=True)
    pos = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Section Settings"
        verbose_name_plural = "Section Settings"

    def __str__(self):
        return f"Section {self.name}"

    @property
    def delta_ta_per_row_value(self):
        if self.delta_ta_per_row:
            return self.delta_ta_per_row
        return 0


class TargetSection(CloneMixin, BaseStateItem):
    class CampaignGrade(models.TextChoices):
        TOP = 'Top', 'Top'
        MIDDLE = 'Middle', 'Middle'
        BOTTOM = 'Bottom', 'Bottom'

    campaign_pos_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE)

    leads_goal = models.PositiveIntegerField('Leads goal', default=0)
    leads_generated = models.PositiveIntegerField('Leads Generated', default=0)
    velocity = models.PositiveIntegerField("Velocity", default=0)
    grade = models.CharField(max_length=16, choices=CampaignGrade.choices, default=CampaignGrade.TOP)
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


class AssetsSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Asset Name", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="assets")
    landing_page = models.FileField("Landing Page", blank=True, null=True)
    titles = models.ManyToManyField(JobTitles, blank=True, related_name="jt_as")
    velocity_koeff = models.FloatField(default=1.0)
    _clone_m2m_fields = [
        "jt_as"
    ]

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.name}"

    @property
    def leads_assets(self):
        return format_leads(self.percent, self.campaign.total_generated)


class IntentFeedsSection(CloneMixin, BaseReportPercentItem):
    class Kinds(models.TextChoices):
        INFUSEMEDIA = 'INFUSEmedia', 'INFUSEmedia'
        BOMBORA = 'Bombora', 'Bombora'
        ABERDEEN = 'Aberdeen', 'Aberdeen'

    name = models.CharField("Intent topic", max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="intents")
    company = models.ManyToManyField(CompanyRef, null=True, blank=True, verbose_name="Companies", related_name="companies")
    kind = models.CharField("Platform", max_length=32, choices=Kinds.choices, default=Kinds.INFUSEMEDIA)
    companies_count = models.PositiveIntegerField("Companies Generated", default=0)

    _clone_m2m_fields = [
        "companies"
    ]

    class Meta:
        verbose_name = "Data Signal Stream"
        verbose_name_plural = "Data Signal Streams"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_generated(self):
        return format_leads(self.percent, self.campaign.done_intent_feed)

    @property
    def goal_intent_feed(self):
        return format_leads(self.percent, self.campaign.total_goal)


class JobTitlesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Name", max_length=200, null=True, blank=True)
    job_title = models.ForeignKey(JobTitles, on_delete=models.CASCADE, verbose_name="Title Captured")
    generated = models.PositiveIntegerField("Leads Generated", default=0)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="titles")
    goal = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_generated(self):
        return format_leads(self.percent, self.campaign.total_goal)


class SuppresionListSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="sups")
    title = models.CharField(max_length=128)
    accounts_value = models.PositiveIntegerField()


class IndustriesSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField(max_length=200, null=True, blank=True)
    industry = models.ForeignKey(Industry, verbose_name="Industry", on_delete=models.CASCADE, related_name="industs")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="industries")

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_industry(self):
        return format_leads(self.percent, self.campaign.total_generated)


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
        return format_leads(self.percent, self.campaign.total_generated)


class RevenueSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("Revenue", max_length=200, blank=True, null=True)
    revenue = models.ForeignKey(Revenue, verbose_name="Revenue Title", on_delete=models.CASCADE, related_name="revens")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="revenues")

    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenue"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_revenue(self):
        return format_leads(self.percent, self.campaign.total_generated)


class CompanySizeSection(CloneMixin, BaseReportPercentItem):
    company_size = models.ForeignKey(CompanySize, verbose_name="Company Size", on_delete=models.CASCADE, related_name="sizes")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="companies")

    class Meta:
        verbose_name = "Company Size"
        verbose_name_plural = "Companies Sizes"

    def __str__(self):
        return f"{self.id}"

    @property
    def leads_company_size(self):
        return format_leads(self.percent, self.campaign.total_generated)


class ABMSection(CloneMixin, BaseReportPercentItem):
    name = models.CharField("ABM", max_length=200, blank=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="abms")
    file = models.FileField("List", null=True, blank=True)
    title = models.CharField(max_length=128)
    accounts_value = models.PositiveIntegerField()

    class Meta:
        verbose_name = "ABM"
        verbose_name_plural = "ABM"

    @property
    def leads(self):
        return format_leads(self.percent, self.campaign.goal_abm)


class FairTradeSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="fair_trades")
    name = models.CharField("Treat Desctiption", max_length=256)
    value = models.CharField("Value", max_length=256)


class InstallBaseSection(CloneMixin, BaseReportPercentItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="ibs")
    name = models.CharField("Title", max_length=256)

    @property
    def leads_installbase (self):
        return format_leads(self.percent, self.campaign.total_generated)
        #return int((self.percent / 100) * self.campaign.total_generated)


class LeadCascadeProgramSection(CloneMixin, BaseReportPercentItem):
    percent = models.FloatField(default=0)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="lead_cascades")
    name = models.CharField("Leads Description", max_length=256)

    @property
    def leads_cascade (self):
        return format_leads(self.percent, self.campaign.total_generated)
        #return int((self.percent / 100) * self.campaign.total_generated)


class NurturingSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="nurturings")
    campaign_type = models.ForeignKey(CampaignTypes, on_delete=models.CASCADE, verbose_name="Type")
    assets = models.ForeignKey(AssetsSection, on_delete=models.CASCADE)
    lead_goal = models.IntegerField(null=True, blank=True)
    nurturing_stages = models.ForeignKey(NurturingStages, on_delete=models.CASCADE)

    @property
    def link(self):
        return self.assets.landing_page.url

    @property
    def generated_leads(self):
        return self.assets.leads_assets


class CreativesSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="creatives")
    subject_line = models.CharField("Subject Line", blank=True, null=True, max_length=128)
    email_text = models.TextField("Email Text", blank=True, null=True)
    landing_page = models.FileField(blank=True, null=True)
    banners = models.FileField(blank=True, null=True)


class ITCuratedSection(CloneMixin, models.Model):
    class Statuses(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSE = 'pause', 'Pause'
        REQUESTED = 'requested', 'Requested'

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="itcurateds")
    status = models.CharField(max_length=16, choices=Statuses.choices, default=Statuses.ACTIVE)
    curated = models.ForeignKey(ITCurated, related_name='curateds', on_delete=models.CASCADE)
    pos = models.SmallIntegerField('Position', default=0)

    def __str__(self):
        return f"{self.curated.title}"


class BANTQuestionsSection(CloneMixin, models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="bants")
    question_txt = models.TextField("Question", null=True, blank=True)
    answer_txt = models.TextField("Answer", null=True, blank=True)
    
    question = models.ForeignKey(BANTQuestion, on_delete=models.CASCADE)

    answer = ChainedForeignKey(
        BANTAnswer,
        chained_field="question",
        chained_model_field="question",
        show_all=False,
        auto_choose=True,
        sort=True
    )

    class Meta:
        verbose_name = "BANT Question"
        verbose_name_plural = "BANT Questions"

    def __str__(self):
        return f"{self.id}"


class CustomQuestionsSection(CloneMixin, BaseStateItem):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="cqs")
    question_txt = models.TextField("Question", null=True, blank=True)
    answer_txt = models.TextField("Answer", null=True, blank=True)
    question = models.ForeignKey(CustomQuestion, on_delete=models.CASCADE)
    answer = ChainedForeignKey(
        CustomAnswer,
        chained_field="question",
        chained_model_field="question",
        show_all=False,
        auto_choose=True,
        sort=True
    )

    class Meta:
        verbose_name = "Custom Question"
        verbose_name_plural = "Custom Questions"

    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    message = models.CharField(max_length=1024, blank=True, null=True)
    manager = models.ForeignKey(Managers, on_delete=models.CASCADE,)


class Teams(CloneMixin, models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="teams", null=True, blank=True)
    name = models.CharField(max_length=250)
    team_lead = models.ForeignKey(Associates, on_delete=models.SET_NULL, related_name='team_lead', null=True, blank=True)
    team_member1 = models.ForeignKey(Associates, on_delete=models.SET_NULL, related_name='member1', null=True, blank=True)
    team_member2 = models.ForeignKey(Associates, on_delete=models.SET_NULL, related_name='member2', null=True, blank=True)
    team_member3 = models.ForeignKey(Associates, on_delete=models.SET_NULL, related_name='member3', null=True, blank=True)
    team_member4 = models.ForeignKey(Associates, on_delete=models.SET_NULL, related_name='member4', null=True, blank=True)
    rejected_percent = models.PositiveIntegerField("% of Leads Rejected", default=0)

    class Meta:
        verbose_name = "Teams"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"{self.name}"

    @property
    def delivered(self):
        cnt = self.campaign.teams.all().count()
        if cnt:
            return self.campaign.total_goal/cnt
        else:
            return 0

    @property
    def rejected(self):
        return self.campaign.total_goal * (self.rejected_percent/100)


@receiver(post_save, sender=Campaign)
def create_curated(sender, instance, created, **kwargs):
    if created:
        for_create = [
            ITCuratedSection(
                campaign=instance, curated=i, pos=i.position
            ) for i in ITCurated.objects.filter(visible=True)
        ]
        ITCuratedSection.objects.bulk_create(for_create)


sections = [

        {'name': ASSETS_NAME, 'slug': ASSETS_SLUG, 'pos': 0, 'delta_v_sector': 1, 'delta_v_per_row': 0},
        {'name': INTENT_FEED_NAME, 'slug': INTENT_FEED_SLUG, 'pos': 1, 'delta_v_sector': 1, 'delta_v_per_row': 0},
        {'name': ABM_NAME, 'slug': ABM_SLUG, 'pos': 2, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},
        {'name': SUPP_LIST_NAME, 'slug': SUPP_LIST_SLUG, 'pos': 3, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},
        {'name': JOB_TITLES_NAME, 'slug': JOB_TITLES_SLUG, 'pos': 4, 'delta_ta_sector': -6, 'delta_ta_per_row': 3},
        {'name': INDUSTRIES_NAME, 'slug': INDUSTRIES_SLUG, 'pos': 5, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},
        {'name': GEO_NAME, 'slug': GEO_SLUG, 'pos': 6, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},
        {'name': REVENUE_NAME, 'slug': REVENUE_SLUG, 'pos': 7, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},
        {'name': COMPANY_SIZE_NAME, 'slug': COMPANY_SIZE_SLUG, 'pos': 8, 'delta_ta_sector': -6, 'delta_ta_per_row': 1},

        {'name': BANT_NAME, 'slug': BANT_SLUG, 'pos': 9, 'delta_v_sector': -1,  'quality_sector': 100, },
        {'name': CQ_NAME, 'slug': CQ_SLUG, 'pos': 10, 'delta_v_sector': 1,  'quality_sector': 25, },
        {'name': INSTALL_BASE_NAME, 'slug': INSTALL_BASE_SLUG, 'pos': 11, 'delta_v_sector': -1, },
        {'name': TACTICS_NAME, 'slug': TACTICS_SLUG, 'pos': 12},
        {'name': ITC_NAME, 'slug': ITC_SLUG, 'pos': 13, 'delta_v_sector': 0,  'delta_ta_sector': 0, 'delta_ta_per_row': 0},
        {'name': FT_NAME, 'slug': FT_SLUG, 'pos': 14, 'delta_v_sector': 1, },
        {'name': LCP_NAME, 'slug': LCP_SLUG, 'pos': 15},
        {'name': NURTURING_NAME, 'slug': NURTURING_SLUG, 'pos': 16, 'delta_v_sector': -1,  'quality_sector': 25, },
        {'name': 'Lets Verify', 'slug': 'lets_verify', 'pos': 17,'delta_v_sector': -3, },
        {'name': CREATIVES_NAME, 'slug': CREATIVES_SLUG, 'pos': 18, 'delta_v_sector': 2, },

    ]


class CampaignClient(Campaign):
    class Meta:
        proxy = True
        verbose_name = "User Campaign"
        verbose_name_plural = "User Campaigns"


@receiver(post_save, sender=Campaign)
def create_settings(sender, instance, created, **kwargs):

    if created:
        for_create = [
            SectionSettings(
                slug=i.get('slug'),
                campaign=instance,
                name=i.get('name'),
                delta_v_sector=i.get('delta_v_sector',0),
                delta_v_per_row=i.get('delta_v_per_row', 0),
                delta_ta_sector=i.get('delta_ta_sector', 0),
                delta_ta_per_row=i.get('delta_ta_per_row', 0),
                quality_sector=i.get('quality_sector'),
                quality_per_row=i.get('quality_per_row'),
            ) for i in sections
        ]
        SectionSettings.objects.bulk_create(for_create)
