from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


from ..models import CampaignTypes, JobTitles, Geolocations, Managers, ITCurated, Revenue, Industry,\
    CompanySize, BANTQuestion, CustomQuestion, IntegrationType, Pacing, CompanyRef, NurturingStages, PartOfMap, Topics

from .serializers import CampaignTypesSerializer, GeolocationsSerializer, JobTitlesSerializer, \
    ManagersSerializer, ITCuratedSerializer, CompanySizeSerializer, RevenueSerializer, IndustrySerializer,\
    CustomQuestionSerializer, BANTQuestionSerializer, IntegrationTypeSerializer, PacingSerializer, CompanyRefSerializer,\
    NurturingStagesSerializer, PartOfMapSerializer, TopicSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,\
    DestroyModelMixin


class ReferencesViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignTypesSerializer

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def nurturing_stages(self, request):
        return Response(data=NurturingStagesSerializer(NurturingStages.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def types(self, request):
        return Response(data=CampaignTypesSerializer(CampaignTypes.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def titles(self, request):
        return Response(data=JobTitlesSerializer(JobTitles.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def geolocations(self, request):
        return Response(data=GeolocationsSerializer(Geolocations.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def revenue(self, request):
        return Response(data=RevenueSerializer(Revenue.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def industry(self, request):
        return Response(data=IndustrySerializer(Industry.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def questions_bant(self, request):
        return Response(
            data=BANTQuestionSerializer(
                BANTQuestion.objects.filter(
                    Q(owner__isnull=True)| Q(owner=self.request.user)
                ).order_by('pos'), many=True
            ).data
        )

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def questions_custom(self, request):
        return Response(
            data=CustomQuestionSerializer(
                CustomQuestion.objects.filter(Q(owner__isnull=True)| Q(owner=self.request.user)), many=True
            ).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def managers(self, request):
        return Response(data=ManagersSerializer(Managers.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def itcurated(self, request):
        return Response(data=ITCuratedSerializer(ITCurated.objects.filter(visible=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def company_size(self, request):
        return Response(data=CompanySizeSerializer(CompanySize.objects.filter(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def integration_types(self, request):
        return Response(data=IntegrationTypeSerializer(IntegrationType.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pacing(self, request):
        return Response(data=PacingSerializer(Pacing.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companies(self, request):
        return Response(data=CompanyRefSerializer(CompanyRef.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def part_of_map(self, request):
        return Response(data=PartOfMapSerializer(PartOfMap.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def topics(self, request):
        return Response(data=TopicSerializer(Topics.objects.all(), many=True).data)
