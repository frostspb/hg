from hourglass.contrib.rest import OptionalSlashDefaultRouter

from hourglass.clients.api.views import ClientsViewSet
from hourglass.campaigns.api.views import CampaignViewSet
from hourglass.references.api.views import ReferencesViewSet

router = OptionalSlashDefaultRouter()

router.register("client", ClientsViewSet, basename='client')
router.register("campaign", CampaignViewSet, basename='campaign')
router.register("references", ReferencesViewSet, basename='references')

app_name = "api"
urlpatterns = router.urls
