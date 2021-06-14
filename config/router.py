from hourglass.contrib.rest import OptionalSlashDefaultRouter

from hourglass.clients.api.views import ClientsViewSet
from hourglass.campaigns.api.views import CampaignViewSet, CustomQuestionsSectionViewSet, BANTQuestionsSectionViewSet,\
GeolocationsSectionViewSet, CompanySizeSectionViewSet, RevenueSectionViewSet, IndustriesSectionViewSet, \
JobTitlesSectionViewSet,  IntentFeedsSectionViewSet, AssetsSectionViewSet, SectionSettingsViewSet,\
CreativesSectionViewSet, NurturingSectionViewSet, LeadCascadeProgramSectionViewSet, FairTradeSectionViewSet,\
InstallBaseSectionViewSet, ABMSectionViewSet, ITCuratedSectionViewSet

from hourglass.references.api.views import ReferencesViewSet

router = OptionalSlashDefaultRouter()

router.register("client", ClientsViewSet, basename="client")
router.register("campaign", CampaignViewSet, basename="campaign")
router.register("section_settings", SectionSettingsViewSet, basename="section_settings")
router.register("references", ReferencesViewSet, basename="references")
router.register("campaign_settings/custom_questions", CustomQuestionsSectionViewSet, basename="questions")
router.register("campaign_settings/bant_questions", BANTQuestionsSectionViewSet, basename="bant")
router.register("campaign_settings/geolocations", GeolocationsSectionViewSet, basename="geolocations")
router.register("campaign_settings/company_size", CompanySizeSectionViewSet, basename="company_size")
router.register("campaign_settings/revenue", RevenueSectionViewSet, basename="revenue")
router.register("campaign_settings/industries", IndustriesSectionViewSet, basename="industries")
router.register("campaign_settings/titles", JobTitlesSectionViewSet, basename="industries")
router.register("campaign_settings/feed", IntentFeedsSectionViewSet, basename="feed")
router.register("campaign_settings/assets", AssetsSectionViewSet, basename="assets")

router.register("campaign_settings/creatives", CreativesSectionViewSet, basename="creatives")
router.register("campaign_settings/cascade", LeadCascadeProgramSectionViewSet, basename="cascade")
router.register("campaign_settings/nurturing", NurturingSectionViewSet, basename="nurturing")
router.register("campaign_settings/fair_trade", FairTradeSectionViewSet, basename="fair_trade")
router.register("campaign_settings/install_base", InstallBaseSectionViewSet, basename="install_base")
router.register("campaign_settings/abm", ABMSectionViewSet, basename="abm")
router.register("campaign_settings/itcurated", ITCuratedSectionViewSet, basename="itcurated")


app_name = "api"
urlpatterns = router.urls
