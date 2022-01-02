from django.utils import timezone

from digicloud.fetcher.models import RSSFeed, FeedItem


class FeedUpdater:
    def __init__(self, rss_id, new_items: list):
        self.rss_feed = rss_id
        self.items = new_items

    def _item_is_exists(self, item):
        return FeedItem.objects.filter(rss_feed_id=self.rss_feed,
                                       title=item.get('title'),
                                       date=item.get('date'),
                                       link=item.get('link'),
                                       description=item.get('summary'),
                                       author=item.get('author'),
                                       ).exists()

    def _add_new_item(self, item):
        item = FeedItem.objects.create(rss_feed_id=self.rss_feed,
                                       title=item.get('title'),
                                       date=item.get('date'),
                                       link=item.get('link'),
                                       description=item.get('summary'),
                                       author=item.get('author'),
                                       )
        return item

    def _update_last_try_date(self):
        rss = RSSFeed.objects.get(id=self.rss_feed)
        rss.last_try = timezone.now()
        rss.save()

    def update_feeds(self):
        for item in self.items:
            if not self._item_is_exists(item):
                self._add_new_item(item)
            self._update_last_try_date()
