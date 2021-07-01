from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import CampaignTypes, JobTitles, Geolocations, Question, Answers, Managers, ITCurated, Revenue, Industry

from .serializers import CampaignTypesSerializer, GeolocationsSerializer, JobTitlesSerializer, QuestionSerializer, \
    ManagersSerializer, ITCuratedSerializer


class ReferencesViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignTypesSerializer

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
        return Response(data=QuestionSerializer(Question.objects.filter(kind=Question.QuestionKinds.BANT), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def questions_custom(self, request):
        return Response(
            data=QuestionSerializer(Question.objects.filter(kind=Question.QuestionKinds.CUSTOM), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def managers(self, request):
        return Response(data=ManagersSerializer(Managers.objects.all(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def itcurated(self, request):
        return Response(data=ITCuratedSerializer(ITCurated.objects.filter(visible=True), many=True).data)
