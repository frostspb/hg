from rest_framework import serializers

from ..models import HourglassSettings


class HourglassSettingsSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()

    class Meta:
        model = HourglassSettings
        fields = (
            'count',
        )

    def get_count(self, instance):
        return instance.get_value()
