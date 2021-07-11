from rest_framework import serializers


from hourglass.references.models import CampaignTypes, Tactics, JobTitles, Geolocations,  Managers, \
    ITCurated, Revenue, Industry, CompanySize, CustomAnswer, CustomQuestion, BANTQuestion, BANTAnswer
#from hourglass.clients.api.serializers import ClientSerializer


class GeolocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocations
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
        return instance.photo_url


class CampaignTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTypes
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
            'id', 'question', 'answers', 'kind'
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
            'id', 'slug', 'link', 'title'
        )
