from rest_framework.serializers import ModelSerializer

from digicloud.fetcher.models import RSSFeed


class RSSSerializer(ModelSerializer):
    class Meta:
        model = RSSFeed
        exclude = ['created', 'updated', 'removed', 'is_active']
