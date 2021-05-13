from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from hourglass.references.models import CampaignTypes
from hourglass.settings.api.serializers import HourglassSettingsSerializer
from hourglass.settings.models import HourglassSettings
from .serializers import CampaignsSectionSerializer,CampaignSerializer, CampaignTypesSerializer, CampaignCopySerializer
from ..models import Campaign


class CampaignViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.filter(active=True)
    filterset_fields = ('client',)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def types(self, request):
        return Response(data=CampaignTypesSerializer(CampaignTypes.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def copy(self, request, *args, **kwargs):
        serializer = CampaignCopySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({}, status=201)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def active_count(self, request, *args, **kwargs):
        serializer = HourglassSettingsSerializer(HourglassSettings.get_solo())
        return Response(data=serializer.data)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def hourglass(self, request, *args, **kwargs):
        c = self.get_object()
        res = {
            'TA': c.ta,
            'duration': c.duration,
            'state': c.state,
            'velocity': c.velocity,
            'total_goal': c.total_goal,
            'generated': c.generated,
            'generated_pos': c.generated_pos,
        }
        return Response(data=res)

