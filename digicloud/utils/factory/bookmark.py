import factory
from factory.django import DjangoModelFactory

from digicloud.feed_management.models import UserFeedBookmarkItem
from digicloud.utils.factory.article import FeedItemFactory
from digicloud.utils.factory.user import UserFactory


class UserFeedBookmarkItemFactory(DjangoModelFactory):
    class Meta:
        model = UserFeedBookmarkItem

    item = factory.SubFactory(FeedItemFactory)
    user = factory.SubFactory(UserFactory)
