from rest_framework import serializers

from ..models import Campaign, TargetSection
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
        model = TargetSection
        fields = (
            #'campaign_pos_type__name',
            'integration', 'pacing', 'leads_goal', 'leads_generated', 'velocity'
        )


class CampaignSerializer(serializers.ModelSerializer):
    # start_date = serializers.SerializerMethodField()
    # end_date = serializers.SerializerMethodField()
    #pos = CampaignsSectionSerializer(source='campaignpos_set', many=True)
    from django.db import models
    #start_date = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = Campaign
        fields = (
            "id", "client", "created", "active", "customer_information", "contact_name", "email", "note",
            "start_offset", "end_offset", "audience_targeted", "name", "campaign_type", "order",
            "start_date", "end_date", "kind", "state",  "details",   "guarantees"
        )

    # def get_start_date(self, instance):
    #     if instance.is_standard:
    #         return instance.initial_start_date
    #     return instance.start_date
    #
    # def get_end_date(self, instance):
    #     if instance.is_standard:
    #         return instance.initial_end_date
    #     return instance.end_date
