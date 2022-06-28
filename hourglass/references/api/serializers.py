from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.conf import settings

from hourglass.references.models import CampaignTypes,  JobTitles, Geolocations,  Managers, \
    ITCurated, Revenue, Industry, CompanySize, CustomAnswer, CustomQuestion, BANTQuestion, BANTAnswer,\
    IntegrationType, Pacing, Associates, CompanyRef, NurturingStages, PartOfMap, Topics, Seniority, LeadType


class AssociatesSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Associates
        fields = (
            'id', 'name', 'photo_url'
        )

    def get_photo_url(self, instance):
        if instance.image:
            photo_url = instance.image.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class GeolocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocations
        fields = (
            'id', 'name', 'code'
        )


class SenioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Seniority
        fields = (
            'id', 'seniority_title'
        )


class LeadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadType
        fields = (
            'lead_type', 'id'
        )

class CompanyRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRef
        fields = (
            'id', 'name',
        )


class CompanySizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySize
        fields = (
            'id', 'name',
        )


class JobTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitles
        fields = (
            'id', 'name',
        )


class ManagersSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Managers
        fields = (
            'id', 'name', 'photo_url'
        )

    def get_photo_url(self, instance):
        if instance.photo:
            photo_url = instance.photo.url
            return f"{settings.STORAGE_ADDR}{photo_url}"


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
        fields = (
            'id', 'name',
        )


class NurturingStagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurturingStages
        fields = (
            'id', 'name',
        )


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = (
            'id', 'name',
        )


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = (
            'id', 'name',
        )


class BANTAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BANTAnswer
        fields = (
            'id', 'answer', 'preferred'
        )


class BANTQuestionSerializer(serializers.ModelSerializer):
    answers = BANTAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = BANTQuestion
        fields = (
            'id', 'question', 'answers', 'kind', 'pos'
        )


class BANTAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BANTAnswer
        fields = (
            'answer',
        )


class BANTQuestionCreateSerializer(WritableNestedModelSerializer):
    answers = BANTAnswerCreateSerializer(many=True, allow_null=True)

    class Meta:
        model = BANTQuestion
        fields = (
            'question', 'answers', 'pos', 'kind'
        )


class BANTQuestionUpdateSerializer(serializers.Serializer):
    answer = serializers.IntegerField()
    question = serializers.IntegerField()


class CQQuestionUpdateSerializer(serializers.Serializer):
    answer = serializers.IntegerField()
    question = serializers.IntegerField()
    state = serializers.CharField()


class CustomAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAnswer
        fields = (
            'answer',
        )


class CustomQuestionCreateSerializer(WritableNestedModelSerializer):
    answers = CustomAnswerCreateSerializer(many=True, allow_null=True)

    class Meta:
        model = CustomQuestion
        fields = (
            'question', 'answers'
        )


class CustomAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAnswer
        fields = (
            'id', 'answer', 'preferred'
        )


class CustomQuestionSerializer(serializers.ModelSerializer):
    answers = CustomAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = CustomQuestion
        fields = (
            'id', 'question', 'answers',
        )


class ITCuratedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITCurated
        fields = (
            'id', 'slug', 'link', 'title', 'position'
        )


class IntegrationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationType
        fields = (
            'id', 'name', 'image', 'image_popup'
        )


class PacingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacing
        fields = (
            'id', 'name'
        )


class PartOfMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfMap
        fields = (
            'id', 'name'
        )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = (
            'id', 'topic'
        )
