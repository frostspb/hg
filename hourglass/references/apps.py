from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReferencesConfig(AppConfig):
    name = "hourglass.references"
    verbose_name = _("References")
