from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from hourglass.references.models import CampaignTypes, JobTitles, Geolocations
from hourglass.settings.api.serializers import HourglassSettingsSerializer
from hourglass.settings.models import HourglassSettings
from .serializers import TargetSectionSerializer, CampaignSerializer,\
    CampaignTypesSerializer, CampaignCopySerializer, SectionsSettingsSerializer, HourglassSerializer,\
    CampaignSettingsSerializer, GeolocationsSerializer, JobTitlesSerializer
from ..models import Campaign


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

