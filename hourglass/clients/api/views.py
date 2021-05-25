from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ClientSerializer, CompanySerializer
from ..models import Client


class ClientsViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.filter(active=True)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def company(self, request, *args, **kwargs):
        return Response(data=CompanySerializer(self.get_object().company_set.all(), many=True).data)
