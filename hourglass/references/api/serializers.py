from rest_framework import serializers


from hourglass.references.models import CampaignTypes, Tactics, JobTitles, Geolocations, Answers, Question
#from hourglass.clients.api.serializers import ClientSerializer

class GeolocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocations
        fields = (
            'id', 'name',
        )


class JobTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitles
        fields = (
            'id', 'name',
        )


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
        fields = (
            'id', 'name',
        )

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = (
            'id', 'value',
        )

class QuestionSerializer(serializers.ModelSerializer):
    answer_variants = AnswerSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = (
            'id', 'name', 'answer_variants',
        )