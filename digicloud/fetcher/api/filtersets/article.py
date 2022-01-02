from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter
from digicloud.fetcher.models import FeedItem


class RSSFeedItemFilterSet(FilterSet):
    category = NumberFilter(field_name='rss_feed__category', lookup_expr='exact')

    class Meta:
        model = FeedItem
        fields = ['rss_feed']
