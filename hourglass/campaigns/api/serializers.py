from rest_framework import serializers

from ..models import Campaign, CampaignsSection
from hourglass.references.models import CampaignTypes


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
        fields = (
            'id', 'name',
        )


class CampaignCopySerializer(serializers.Serializer):
    source_id = serializers.IntegerField(required=True)

    class Meta:
        fields = (
            'source_id',
        )

    def save(self, **kwargs):
        source_id = self.validated_data.get('source_id')
        campaign = Campaign.objects.filter(id=source_id).first()
        if not campaign:
            return
        return Campaign.objects.copy(campaign)


class CampaignsSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignsSection
        fields = (
            #'campaign_pos_type__name',
            'integration', 'pacing', 'leads_goal', 'leads_generated', 'velocity'
        )


class CampaignSerializer(serializers.ModelSerializer):
    #start_date = serializers.SerializerMethodField()
    #end_date = serializers.SerializerMethodField()
    #pos = CampaignsSectionSerializer(source='campaignpos_set', many=True)

    class Meta:
        model = Campaign
        fields = (
            "id", "client", "created", "active", "customer_information", "contact_name", "email", "note",
            "start_offset", "end_offset", "audience_targeted",
            "start_date", "end_date", "kind", "state", #"pos"
        )

    # def get_start_date(self, instance):
    #     return instance.start_date
    #
    # def get_end_date(self, instance):
    #     return instance.end_date
