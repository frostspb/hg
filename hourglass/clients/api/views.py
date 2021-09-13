from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .serializers import ClientSerializer, CompanySerializer
from ..models import Client


class ClientsViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.filter(active=True)

    def get_queryset(self):
        return self.queryset.filter(Q(owner__isnull=True) | Q(owner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def company(self, request, *args, **kwargs):
        return Response(data=CompanySerializer(self.get_object().company_set.all(), many=True).data)
