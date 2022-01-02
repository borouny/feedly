from django_filters.rest_framework import FilterSet
from digicloud.feed_management.models import Comment


class CommentFilterSet(FilterSet):
    class Meta:
        model = Comment
        fields = ['user', 'feed_item']
