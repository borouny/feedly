from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from digicloud.feed_management.models import UserFeedBookmarkItem
from digicloud.fetcher.api.serializers.website import RSSSerializer


class UserFeedBookmarkItemSerializer(ModelSerializer):
    title = serializers.CharField(source='item.title')
    description = serializers.CharField(source='item.description')
    date = serializers.DateTimeField(source='item.date')
    link = serializers.URLField(source='item.link')
    author = serializers.URLField(source='item.author')
    rss_feed = RSSSerializer(source='item.rss_feed')
    item_id = serializers.IntegerField(source='item.id')

    class Meta:
        model = UserFeedBookmarkItem
        exclude = ['user', 'item']


class UpdatableUserFeedBookmarkItemSerializer(ModelSerializer):
    class Meta:
        model = UserFeedBookmarkItem
        fields = ['item', 'user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UserFeedBookmarkItem.objects.all(),
                fields=['item', 'user'],
                message="This user bookmark this item before."
            )
        ]

    def create(self, validated_data, user=None):
        return UserFeedBookmarkItem.objects.create(item=validated_data['item'], user=user)
