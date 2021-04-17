from hourglass.contrib.rest import OptionalSlashDefaultRouter

from hourglass.clients.api.views import ClientsViewSet
from hourglass.campaigns.api.views import CampaignTemplateViewSet

router = OptionalSlashDefaultRouter()

router.register("client", ClientsViewSet, basename='client')
router.register("campaign", CampaignTemplateViewSet, basename='campaign')

app_name = "api"
urlpatterns = router.urls
