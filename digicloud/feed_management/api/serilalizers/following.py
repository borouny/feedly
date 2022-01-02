from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from digicloud.feed_management.models import FollowedRSSFeed
from digicloud.fetcher.api.serializers.website import RSSSerializer


class FollowingSerializer(ModelSerializer):
    class Meta:
        model = FollowedRSSFeed
        fields = ['rss_feed', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=FollowedRSSFeed.objects.all(),
                fields=['rss_feed', 'user']
            )
        ]

    def create(self, validated_data, user=None):
        return FollowedRSSFeed.objects.create(rss_feed=validated_data['rss_feed'], user=user)


class ReadOnlyFollowingSerializer(ModelSerializer):
    rss_feed = RSSSerializer()

    class Meta:
        model = FollowedRSSFeed
        fields = '__all__'
