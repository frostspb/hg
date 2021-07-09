from rest_framework import serializers
from django.conf import settings
from ..models import Client, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class ClientSerializer(serializers.ModelSerializer):
    current_leads_goals = serializers.SerializerMethodField()
    current_campaigns = serializers.SerializerMethodField()
    client_since = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id', 'name', 'client_type', 'total_campaigns', 'leads_generated', 'client_since',
            'current_leads_goals', 'current_campaigns',
        )

    def get_client_since(self, instance):
        if instance.client_since:
            return instance.client_since.strftime(settings.ENDPOINT_DATE_FORMAT)

    def get_current_leads_goals(self, instance):
        return instance.current_leads_goals

    def get_current_campaigns(self, instance):
        return instance.current_campaigns



