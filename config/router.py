from hourglass.contrib.rest import OptionalSlashDefaultRouter

from hourglass.clients.api.views import ClientsViewSet
from hourglass.campaigns.api.views import CampaignViewSet

router = OptionalSlashDefaultRouter()

router.register("client", ClientsViewSet, basename='client')
router.register("campaign", CampaignViewSet, basename='campaign')

app_name = "api"
urlpatterns = router.urls
