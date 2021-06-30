import logging
from django.db import models

logger = logging.getLogger(__name__)

WHITELIST = [
    "bants", "cqs", "geolocations", "companies", "revenues", "industries",
    "intents", "titles", "assets", "campaigns",
]


class CampaignsManager(models.Manager):
    def copy(self, source_campaign, destination_client_id=None):
        copy_cmp = source_campaign.make_clone()
        if copy_cmp:
            copy_cmp.kind = type(copy_cmp).CampaignKinds.USER
            copy_cmp.state = type(copy_cmp).States.STATE_PAUSE
            if destination_client_id:
                copy_cmp.client_id = destination_client_id
            copy_cmp.save()
