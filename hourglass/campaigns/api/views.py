from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,\
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from hourglass.references.models import CampaignTypes, JobTitles, Geolocations
from hourglass.settings.api.serializers import HourglassSettingsSerializer
from hourglass.settings.models import HourglassSettings
from .serializers import TargetSectionSerializer, CampaignSerializer , AssetsSectionSerializer,\
    CampaignTypesSerializer, CampaignCopySerializer, SectionsSettingsSerializer, HourglassSerializer,\
    CampaignSettingsSerializer, GeolocationsSectionSerializer, JobTitlesSerializer,CustomQuestionsSectionSerializer,\
    CustomQuestionsSection, BANTQuestionsSectionSerializer, GeolocationsSectionSerializer,\
    CompanySizeSectionSerializer, RevenueSectionSerializer, IndustriesSectionSerializer,\
    JobTitlesSectionSerializer, IntentFeedsSectionSerializer, ABMSectionSerializer,\
    InstallBaseSectionSerializer, FairTradeSectionSerializer,LeadCascadeProgramSectionSerializer,\
    NurturingSectionSerializer, CreativesSectionSerializer, ITCuratedSectionSerializer

from ..models import Campaign, TargetSection, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection


class CampaignViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.filter(active=True)
    filterset_fields = ('client',)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def integration_types(self, request):
        return Response(data=Campaign.IntegrationTypes.choices)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pacing(self, request):
        return Response(data=Campaign.PacingTypes.choices)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def kinds(self, request):
        return Response(data=Campaign.CampaignKinds.choices)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def copy(self, request, *args, **kwargs):
        serializer = CampaignCopySerializer(data={}, context={'campaign': self.get_object()})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({}, status=201)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def active_count(self, request, *args, **kwargs):
        serializer = HourglassSettingsSerializer(HourglassSettings.get_solo())
        return Response(data=serializer.data)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def hourglass(self, request, *args, **kwargs):
        return Response(data=HourglassSerializer(self.get_object()).data)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def settings_campaign(self, request, *args, **kwargs):
        return Response(data=CampaignSettingsSerializer(self.get_object()).data)


class SectionSettingsViewSet(UpdateModelMixin,  RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SectionsSettingsSerializer
    queryset = SectionSettings.objects.all()


class AssetsSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = AssetsSectionSerializer
    queryset = AssetsSection.objects.all()
    filterset_fields = ('campaign',)


class IntentFeedsSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = IntentFeedsSectionSerializer
    queryset = IntentFeedsSection.objects.all()
    filterset_fields = ('campaign', 'kind')


class JobTitlesSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = JobTitlesSectionSerializer
    queryset = JobTitlesSection.objects.all()
    filterset_fields = ('campaign',)


class IndustriesSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = IndustriesSectionSerializer
    queryset = IndustriesSection.objects.all()
    filterset_fields = ('campaign',)


class RevenueSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = RevenueSectionSerializer
    queryset = RevenueSection.objects.all()
    filterset_fields = ('campaign',)


class CompanySizeSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySizeSectionSerializer
    queryset = CompanySizeSection.objects.all()
    filterset_fields = ('campaign',)


class GeolocationsSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = GeolocationsSectionSerializer
    queryset = GeolocationsSection.objects.all()
    filterset_fields = ('campaign',)


class BANTQuestionsSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = BANTQuestionsSectionSerializer
    queryset = BANTQuestionsSection.objects.all()
    filterset_fields = ('campaign',)


class CustomQuestionsSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomQuestionsSectionSerializer
    queryset = CustomQuestionsSection.objects.all()
    filterset_fields = ('campaign',)


class ABMSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ABMSectionSerializer
    queryset = ABMSection.objects.all()
    filterset_fields = ('campaign',)


class InstallBaseSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = InstallBaseSectionSerializer
    queryset = InstallBaseSection.objects.all()
    filterset_fields = ('campaign',)


class FairTradeSectionViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = FairTradeSectionSerializer
    queryset = FairTradeSection.objects.all()
    filterset_fields = ('campaign',)


class LeadCascadeProgramSectionViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet,
                                    CreateModelMixin,
                                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadCascadeProgramSectionSerializer
    queryset = LeadCascadeProgramSection.objects.all()
    filterset_fields = ('campaign',)


class NurturingSectionViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet,
                                    CreateModelMixin,
                                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = NurturingSectionSerializer
    queryset = NurturingSection.objects.all()
    filterset_fields = ('campaign',)


class CreativesSectionViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet,
                                    CreateModelMixin,
                                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CreativesSectionSerializer
    queryset = CreativesSection.objects.all()
    filterset_fields = ('campaign',)


class ITCuratedSectionViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet,
                                    CreateModelMixin,
                                    DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ITCuratedSectionSerializer
    queryset = ITCuratedSection.objects.all()
    filterset_fields = ('campaign',)