from rest_framework.serializers import ModelSerializer

from digicloud.fetcher.models import FeedItem


class RSSItemSerializer(ModelSerializer):
    class Meta:
        model = FeedItem
        exclude = ['rss_feed']


class RSSPureItemSerializer(ModelSerializer):
    class Meta:
        model = FeedItem
        fields = '__all__'
