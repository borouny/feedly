import factory
from factory.django import DjangoModelFactory

from digicloud.feed_management.models import FollowedRSSFeed
from digicloud.utils.factory.rss import RSSFeedFactory
from digicloud.utils.factory.user import UserFactory


class FollowedRSSFeedFactory(DjangoModelFactory):
    class Meta:
        model = FollowedRSSFeed

    rss_feed = factory.SubFactory(RSSFeedFactory)
    user = factory.SubFactory(UserFactory)
