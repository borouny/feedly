from django.db import models
from django.utils import timezone

from digicloud.fetcher.models import FeedItem, RSSFeed
from digicloud.user_management.models import User
from digicloud.utils.models import TrackedModel


class UserFeedBookmarkItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='items', db_index=True)
    item = models.ForeignKey(FeedItem, on_delete=models.CASCADE, blank=True, null=True, related_name='items')


class Comment(TrackedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', db_index=True)
    feed_item = models.ForeignKey(FeedItem, on_delete=models.CASCADE, related_name='comments', db_index=True)
    title = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(null=False, blank=False)


class FollowedRSSFeed(models.Model):
    created = models.DateTimeField('Creation time', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='followings',
                             db_index=True)
    rss_feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE, blank=False, null=False, related_name='followers')
