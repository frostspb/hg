from django_filters import rest_framework as filters
from django_filters.fields import ModelMultipleChoiceField
from django_filters.constants import EMPTY_VALUES
from hourglass.clients.models import Client
from .models import Campaign


class CampaignFilter(filters.FilterSet):
    # genres = GenresFilter(
    #     field_name='genres__name',
    #     to_field_name='name',
    #     queryset=Genre.objects.all(),
    # )

    # o = OrderingWithCreatedFilter(
    #     fields=['created', 'date_launch', 'priority', 'name'],
    # )
    # gamepass = filters.NumberFilter(field_name='gamepasses__id',)
    search = filters.CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Campaign
        fields = ['genres', 'is_sellable', 'o', 'search', 'gamepass']