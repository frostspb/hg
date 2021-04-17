from rest_framework import serializers

from ..models import CampaignTemplate, CampaignTemplatePos, CampaignTypes


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
        fields = (
            'id', 'name',
        )


class CampaignTemplatePosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTemplatePos
        fields = (
            'campaign_type', 'integration', 'pacing', 'leads_goal', 'leads_generated', 'velocity'
        )


class CampaignTemplateSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    pos = CampaignTemplatePosSerializer(source='campaigntemplatepos_set', many=True)

    class Meta:
        model = CampaignTemplate
        fields = (
            'id', 'client', 'start_date', 'end_date', 'audience_targeted', 'pos',
        )

    def get_start_date(self, instance):
        return instance.start_date

    def get_end_date(self, instance):
        return instance.end_date
