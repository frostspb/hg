from rest_framework import serializers

from ..models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id', 'name', 'client_type', 'total_campaigns', 'leads_generated', 'client_since',
        )
