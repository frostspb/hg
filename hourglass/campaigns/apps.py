from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CampaignsConfig(AppConfig):
    name = "hourglass.campaigns"
    verbose_name = _("Campaigns")
