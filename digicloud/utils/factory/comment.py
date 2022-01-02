import factory
from factory.django import DjangoModelFactory

from digicloud.feed_management.models import Comment
from digicloud.utils.factory.article import FeedItemFactory
from digicloud.utils.factory.user import UserFactory


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    title = factory.Sequence(lambda n: 'title%d' % n)
    description = factory.Sequence(lambda n: 'description%d' % n)
    user = factory.SubFactory(UserFactory)
    feed_item = factory.SubFactory(FeedItemFactory)
