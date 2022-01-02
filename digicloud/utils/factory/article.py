import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from digicloud.fetcher.models import FeedItem
from digicloud.utils.factory.rss import RSSFeedFactory


class FeedItemFactory(DjangoModelFactory):
    class Meta:
        model = FeedItem

    link = factory.Sequence(lambda n: 'http://google%s.com' % n)
    title = factory.Sequence(lambda n: 'title%d' % n)
    description = factory.Sequence(lambda n: 'description%d' % n)
    author = factory.Sequence(lambda n: 'author%d' % n)
    rss_feed = factory.SubFactory(RSSFeedFactory)
    date = timezone.now()
