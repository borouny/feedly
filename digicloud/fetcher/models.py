from django.utils import timezone
from django.db import models

from digicloud.utils.models import TrackedModel


class FeedVersion(models.IntegerChoices):
    rss20 = 0, 'rss20'
    atom10 = 1, 'atom10'


class Category(models.IntegerChoices):
    tech = 0, 'tech'
    programming = 1, 'programming'
    economy = 2, 'economy'
    business = 4, 'business'
    science = 5, 'science'
    culture = 6, 'culture'


class RSSFeed(TrackedModel):
    url = models.URLField(null=False, blank=False, db_index=True)
    feed_version = models.PositiveSmallIntegerField(choices=FeedVersion.choices)
    category = models.PositiveSmallIntegerField(choices=Category.choices, null=True, blank=True)
    last_try = models.DateTimeField(null=True)
    name = models.CharField(max_length=500)

    def set_try_date(self):
        self.last_try = timezone.now()
        self.save()


class FeedItem(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateTimeField(max_length=500, null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=500, null=True, blank=True)
    rss_feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE, blank=True, null=True, related_name='items',
                                 db_index=True)
