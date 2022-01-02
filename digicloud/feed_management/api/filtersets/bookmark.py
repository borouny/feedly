from django_filters.rest_framework import FilterSet
from django_filters import CharFilter, DateTimeFilter

from digicloud.feed_management.models import UserFeedBookmarkItem


class UserFeedBookmarkItemFilterSet(FilterSet):
    rss = CharFilter(field_name='item__rss_feed', lookup_expr='exact')
    start_date = DateTimeFilter(field_name='item__date', lookup_expr='gt')
    end_date = DateTimeFilter(field_name='item__date', lookup_expr='lt')

    class Meta:
        model = UserFeedBookmarkItem
        fields = []
