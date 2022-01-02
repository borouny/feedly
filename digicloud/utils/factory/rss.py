import factory
from factory.django import DjangoModelFactory

from digicloud.fetcher.models import RSSFeed, FeedVersion, Category


class RSSFeedFactory(DjangoModelFactory):
    class Meta:
        model = RSSFeed

    url = factory.Sequence(lambda n: 'http://google%s.com' % n)
    name = factory.Sequence(lambda n: 'havig%d' % n)
    feed_version = FeedVersion.atom10.value
    category = Category.tech.value
