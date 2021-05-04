from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SettingsConfig(AppConfig):
    name = "hourglass.settings"
    verbose_name = _("Settings")
