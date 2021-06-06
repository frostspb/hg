from hourglass.contrib.rest import OptionalSlashDefaultRouter

from hourglass.clients.api.views import ClientsViewSet
from hourglass.campaigns.api.views import CampaignViewSet, CustomQuestionsSectionViewSet, BANTQuestionsSectionViewSet,\
GeolocationsSectionViewSet, CompanySizeSectionViewSet, RevenueSectionViewSet, IndustriesSectionViewSet, \
JobTitlesSectionViewSet,  IntentFeedsSectionViewSet, AssetsSectionViewSet

from hourglass.references.api.views import ReferencesViewSet

router = OptionalSlashDefaultRouter()

router.register("client", ClientsViewSet, basename="client")
router.register("campaign", CampaignViewSet, basename="campaign")
router.register("campaign/references", ReferencesViewSet, basename="references")
router.register("campaign/custom_questions", CustomQuestionsSectionViewSet, basename="questions")
router.register("campaign/bant_questions", BANTQuestionsSectionViewSet, basename="bant")
router.register("campaign/geolocations", GeolocationsSectionViewSet, basename="geolocations")
router.register("campaign/company_size", CompanySizeSectionViewSet, basename="company_size")
router.register("campaign/revenue", RevenueSectionViewSet, basename="revenue")
router.register("campaign/industries", IndustriesSectionViewSet, basename="industries")
router.register("campaign/titles", JobTitlesSectionViewSet, basename="industries")
router.register("campaign/feed", IntentFeedsSectionViewSet, basename="feed")
router.register("campaign/assets", AssetsSectionViewSet, basename="assets")


app_name = "api"
urlpatterns = router.urls
