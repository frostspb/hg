from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientsConfig(AppConfig):
    name = "hourglass.clients"
    verbose_name = _("Clients")
