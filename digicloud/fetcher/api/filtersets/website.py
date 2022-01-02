from django_filters.rest_framework import FilterSet
from digicloud.fetcher.models import RSSFeed


class RSSFeedFilterSet(FilterSet):
    class Meta:
        model = RSSFeed
        fields = ['url', 'category', 'name']
