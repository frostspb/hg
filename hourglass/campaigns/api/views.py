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
    MessageSerializer, CampaignCreateSerializer, NurturingCreateSectionSerializer, CampaignListSerializer,\
    ITCuratedUpdateStatusSerializer, SettingsUpdateStatusSerializer


from ..models import Campaign, SectionSettings,  AssetsSection, IntentFeedsSection, JobTitlesSection, \
    IndustriesSection, RevenueSection, CompanySizeSection, GeolocationsSection, BANTQuestionsSection, \
    CustomQuestionsSection, ABMSection, InstallBaseSection, FairTradeSection, \
    LeadCascadeProgramSection, NurturingSection, CreativesSection, ITCuratedSection, SuppresionListSection, Message

from django.http import QueryDict
import json
from rest_framework import parsers


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}
        # find the data field and parse it
        data = json.loads(result.data["data"])
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)


class CampaignViewSet(ListModelMixin, UpdateModelMixin,  RetrieveModelMixin, GenericViewSet, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.filter(active=True)
    filterset_fields = ('client',)
    parser_classes = (MultipartJsonParser, parsers.JSONParser)

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

        if serializer.data.get('kind') == Campaign.CampaignKinds.CONTRACT:
            #obj = Campaign.objects.filter(id=serializer.data.get('id')).first()

            email = self.request.user.email
            order = serializer.data.get('order', '')
            note = serializer.data.get('note', '')
            guarantees = serializer.data.get('guarantees', '')
            details = serializer.data.get('details', '')
            customer_information = serializer.data.get('customer_information', '')
            contact_name = serializer.data.get('contact_name', '')
            name = serializer.data.get('name', '')
            email_field = serializer.data.get('email', '')
            start_date = serializer.data.get('start_date', '')
            end_date = serializer.data.get('end_date', '')
            campaign_type = serializer.data.get('campaign_type', '')
            if email:
                msg = f"Customer information {customer_information} \n" \
                      f"Contact name {contact_name} \n" \
                      f"Campaign name {name} \n " \
                      f"Email {email_field} \n" \
                      f"Campaign start date {start_date} \n" \
                      f"Campaign end date {end_date} \n" \
                      f"Campaign type {campaign_type} \n" \
                      f"Purchase order {order} \n" \
                      f"Campaign guarantees {guarantees} \n" \
                      f"Campaign details {details} \n" \
                      f"Notes {note} \n"
                send_status_email.delay(subj='Hourglass', to=[email], msg=msg, addr_from=settings.MAIL_FROM)

        if serializer.data.get('kind') == Campaign.CampaignKinds.USER:
            email = self.request.user.email
            if email:
                msg = f"You have just save the new Campaign. Thank you. Campaign name: {serializer.data.get('name', '')}"
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

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def campaign_list(self, request, *args, **kwargs):
        srz = CampaignListSerializer(self.queryset, many=True)
        return Response(data=srz.data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_cq(self, request, *args, **kwargs):
        from hourglass.references.api.serializers import CustomQuestionCreateSerializer, CustomQuestionSerializer
        srz = CustomQuestionCreateSerializer(data=request.data)
        srz.is_valid()
        x = srz.save()
        x.campaign = self.get_object()
        x.save()

        return Response(CustomQuestionSerializer(x).data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def load_creatives_files(self, request, *args, **kwargs):
        from hourglass.references.api.serializers import CustomQuestionCreateSerializer, CustomQuestionSerializer
        srz = CustomQuestionCreateSerializer(data=request.data)
        srz.is_valid()
        x = srz.save()
        x.campaign = self.get_object()
        x.save()

        return Response(CustomQuestionSerializer(x).data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_bant(self, request, *args, **kwargs):
        from hourglass.references.api.serializers import BANTQuestionCreateSerializer, BANTQuestionSerializer
        srz = BANTQuestionCreateSerializer(data=request.data)
        srz.is_valid()
        x = srz.save()
        x.campaign = self.get_object()
        x.save()

        return Response(BANTQuestionSerializer(x).data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def update_bant(self, request, *args, **kwargs):
        c = self.get_object()
        from hourglass.references.api.serializers import BANTQuestionUpdateSerializer
        srz = BANTQuestionUpdateSerializer(data=request.data, many=True)
        srz.is_valid()
        data = srz.data

        for i in data:
            BANTQuestionsSection.objects.create(
                campaign=c,
                question_id=i.get('question'),
                answer_id=i.get('answer')
            )
        return Response({})

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def update_cq(self, request, *args, **kwargs):
        c = self.get_object()
        from hourglass.references.api.serializers import BANTQuestionUpdateSerializer
        srz = BANTQuestionUpdateSerializer(data=request.data, many=True)
        srz.is_valid()
        data = srz.data

        for i in data:
            if i.get('question') and i.get('question'):
                CustomQuestionsSection.objects.create(
                    campaign=c,
                    question_id=i.get('question'),
                    answer_id=i.get('answer')
                )
        return Response({})

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def update_curated(self, request, *args, **kwargs):
        srz = ITCuratedUpdateStatusSerializer(data=request.data, many=True)
        srz.is_valid()
        data = srz.data
        for i in data:
            sec = ITCuratedSection.objects.filter(pk=i.get('id')).first()
            if sec:
                sec.status = i.get('status')
                sec.save(update_fields=['status'])
        return Response({})

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def update_settings(self, request, *args, **kwargs):
        srz = SettingsUpdateStatusSerializer(data=request.data, many=True)
        srz.is_valid()
        data = srz.data
        c = self.get_object()
        for i in data:
            sec = SectionSettings.objects.filter(campaign=c, slug=i.get('slug')).first()
            if sec:
                sec.enabled = i.get('enabled')
                sec.save(update_fields=['enabled'])
        return Response({})




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
            send_status_email.delay(subj='Hourglass', to=[email], msg=msg, addr_from=settings.MAIL_FROM)

from rest_framework import views


class CFilesUpload(views.APIView):
    def post(self, request):
        campaign = request.POST.get('campaign')
        if campaign:
            cmp = Campaign.objects.filter(id=campaign).first()
            if not cmp:
                return Response({})

            for file in request.FILES:
                _f = request.FILES.get(file)
                prefix, sect_id = file.split('_')
                if 'banner' in prefix:
                    x = CreativesSection.objects.filter(campaign=cmp, id = int(sect_id)).first()
                    x.banners = _f
                    x.save()

                if 'landing' in prefix:
                    x = CreativesSection.objects.filter(campaign=cmp, id=int(sect_id)).first()
                    x.landing_page = _f
                    x.save()
        return Response({})
