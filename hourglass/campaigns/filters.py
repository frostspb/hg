from django_filters import rest_framework as filters

from .models import Campaign


class CampaignFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Campaign
        fields = ['genres', 'is_sellable', 'o', 'search', 'gamepass']
