from rest_framework import serializers

from ..models import Client


class ClientSerializer(serializers.ModelSerializer):
    current_leads_goals = serializers.SerializerMethodField()
    current_campaigns = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id', 'name', 'client_type', 'total_campaigns', 'leads_generated', 'client_since',
            'current_leads_goals', 'current_campaigns',
        )

    def get_current_leads_goals(self, instance):
        return instance.current_leads_goals

    def get_current_campaigns(self, instance):
        return instance.current_campaigns
