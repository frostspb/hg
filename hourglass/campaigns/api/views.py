from random import choice
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,\
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q

from hourglass.references.models import  Managers
from hourglass.campaigns.tasks import send_status_email
from hourglass.settings.api.serializers import HourglassSettingsSerializer
from hourglass.settings.models import HourglassSettings
from .serializers import CampaignSerializer, AssetsSectionSerializer,\
    CampaignCopySerializer, SectionsSettingsSerializer, HourglassSerializer,\
    CampaignSettingsSerializer, CustomQuestionsSectionSerializer,\
    BANTQuestionsSectionSerializer, GeolocationsSectionSerializer,\
    CompanySizeSectionSerializer, RevenueSectionSerializer, IndustriesSectionSerializer,\
    JobTitlesSectionSerializer, IntentFeedsSectionSerializer, ABMSectionSerializer,\
    InstallBaseSectionSerializer, FairTradeSectionSerializer,LeadCascadeProgramSectionSerializer,\
    NurturingSectionSerializer, CreativesSectionSerializer, ITCuratedSectionSerializer, SuppresionListSectionSerializer,\
    MessageSerializer, CampaignCreateSerializer, NurturingCreateSectionSerializer

from ..models import Campaign, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection, Message


class CampaignViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.filter(active=True)
    filterset_fields = ('client',)

    # def get_serializer_context(self):
    #     context = super(CampaignViewSet, self).get_serializer_context()
    #     context.update({"request": self.request})
    #     return context
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignCreateSerializer
        else:
            return CampaignSerializer

    def get_queryset(self):
        return self.queryset.filter(
            Q(owner__isnull=True, kind=Campaign.CampaignKinds.STANDARD)
            | Q(kind__in=[Campaign.CampaignKinds.USER, Campaign.CampaignKinds.CONTRACT], owner=self.request.user)
        )

    def perform_create(self, serializer):
        manager = choice(Managers.objects.all())
        serializer.save(managed_by=manager, owner=self.request.user)

        if serializer.data.get('kind') == Campaign.CampaignKinds.USER:
            #obj = Campaign.objects.filter(id=serializer.data.get('id')).first()

            email = self.request.user.email
            order = serializer.data.get('order', '')
            note = serializer.data.get('note', '')
            guarantees = serializer.data.get('guarantees', '')
            details = serializer.data.get('details', '')
            customer_information = serializer.data.get('customer_information', '')
            contact_name = serializer.data.get('contact_name', '')
            name = serializer.data.get('name', '')
            start_date = serializer.data.get('start_date', '')
            end_date = serializer.data.get('end_date', '')
            campaign_type = serializer.data.get('campaign_type', '')
            if email:
                msg = f"Customer information {customer_information} \n" \
                      f"Contact name {contact_name} \n" \
                      f"Campaign name {name} \n" \
                      f"Campaign start date {start_date} \n" \
                      f"Campaign end date {end_date} \n" \
                      f"Campaign type {campaign_type} \n" \
                      f"Purchase order {order} \n" \
                      f"Campaign guarantees {guarantees} \n" \
                      f"Campaign details {details} \n" \
                      f"Notes {note} \n"
                send_status_email.delay(subj='Hourglass', to=[email], msg=msg, addr_from=settings.MAIL_FROM)

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

    def get_serializer_class(self):
        if self.action == 'create':
            return NurturingCreateSectionSerializer
        else:
            return NurturingSectionSerializer


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


class SuppresionListSectionViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet,
                                   CreateModelMixin,
                                   DestroyModelMixin
                                   ):
    permission_classes = [IsAuthenticated]
    serializer_class = SuppresionListSectionSerializer
    queryset = SuppresionListSection.objects.all()
    filterset_fields = ('campaign',)


class MessageViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin,
                           DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filterset_fields = ('campaign',)

    def perform_create(self, serializer):
        serializer.save()

        obj = Message.objects.filter(id=serializer.data.get('id')).first()
        email = self.request.user.email
        if obj and email:
            msg = obj.message
            send_status_email.delay(subj='hourglass', to=[email], msg=msg, addr_from=settings.MAIL_FROM)