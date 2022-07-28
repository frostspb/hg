from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters import rest_framework as filters

from rest_framework.pagination import PageNumberPagination
from ..models import CampaignTypes, JobTitles, Geolocations, Managers, ITCurated, Revenue, Industry,\
    CompanySize, BANTQuestion, CustomQuestion, IntegrationType, Pacing, CompanyRef, NurturingStages, PartOfMap, Topics, Seniority, LeadType

from .serializers import CampaignTypesSerializer, GeolocationsSerializer, JobTitlesSerializer, \
    ManagersSerializer, ITCuratedSerializer, CompanySizeSerializer, RevenueSerializer, IndustrySerializer,\
    CustomQuestionSerializer, BANTQuestionSerializer, IntegrationTypeSerializer, PacingSerializer, CompanyRefSerializer,\
    NurturingStagesSerializer, PartOfMapSerializer, TopicSerializer, SenioritySerializer, LeadTypeSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,\
    DestroyModelMixin


class RefFilter(filters.FilterSet):
    topic = filters.CharFilter(method='search_filter', help_text='Поиск по строке')

    class Meta:
        model = Topics
        fields = ['topic',]

    def search_filter(self, queryset, name, value):
        return queryset.filter(topic__icontains=value)


class ReferencesViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignTypesSerializer
    #filterset_fields = ('topic',)

    pagination_class = PageNumberPagination
    #page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
    filterset_class = RefFilter

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def seniority(self, request):
        return Response(data=SenioritySerializer(Seniority.objects.filter(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def lead_types(self, request):
        return Response(data=LeadTypeSerializer(LeadType.objects.filter(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def nurturing_stages(self, request):
        return Response(data=NurturingStagesSerializer(NurturingStages.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def types(self, request):
        return Response(data=CampaignTypesSerializer(CampaignTypes.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def titles(self, request):
        qs = JobTitles.objects.all()
        title = request.GET.get('title')
        if title:
            qs = qs.filter(name__icontains=title)
        return Response(data=JobTitlesSerializer(qs, many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def geolocations(self, request):
        qs = Geolocations.objects.all()
        geolocation = request.GET.get('geolocation')
        if geolocation:
            qs = qs.filter(name__icontains=geolocation)
        return Response(data=GeolocationsSerializer(qs, many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def revenue(self, request):
        return Response(data=RevenueSerializer(Revenue.objects.filter(active=True), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def industry(self, request):
        qs = Industry.objects.filter(active=True)
        industry = request.GET.get('industry')
        if industry:
            qs = qs.filter(name__icontains=industry)
        return Response(data=IndustrySerializer(qs, many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def questions_bant(self, request):
        campaign = request.GET.get('campaign')
        return Response(
            data=BANTQuestionSerializer(
                BANTQuestion.objects.filter(
                    Q(campaign__isnull=True)| Q(campaign__id=campaign)
                ).order_by('pos'), many=True
            ).data
        )

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def questions_custom(self, request):
        campaign = request.GET.get('campaign')
        return Response(
            data=CustomQuestionSerializer(
                CustomQuestion.objects.filter(Q(campaign__isnull=True)| Q(campaign__id=campaign)), many=True
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
        qs = self.filter_queryset(Topics.objects.all())
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = TopicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TopicSerializer(qs, many=True)
        return Response(data=serializer.data)
