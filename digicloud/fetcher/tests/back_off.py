from digicloud.fetcher.models import RSSFeed
from django.utils import timezone
from datetime import timedelta

from django.test import TestCase
from digicloud.celery import app
from digicloud.fetcher.models import FeedItem
from digicloud.fetcher.services.feed_updater import FeedUpdater
from digicloud.fetcher.services.rss_reader import RSSReaderService
from digicloud.fetcher.tasks import get_new_rss
from digicloud.fetcher.tests import parsed_data
from digicloud.utils.factory.rss import RSSFeedFactory


class TestBackoffWorker(TestCase):

    def setUp(self):
        self.parsed_feed = parsed_data
        self.parsed_feed_item = RSSReaderService(self.parsed_feed).read_rss()
        self.rss_1 = RSSFeedFactory()
        self.rss_2 = RSSFeedFactory()
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.rss = RSSFeedFactory()

    def test_feed_item_count(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        self.assertEqual(FeedItem.objects.all().count(), 10)

    def test_duplicate_feed_item(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        self.assertEqual(FeedItem.objects.all().count(), 10)

    def test_feed_item_specific_rss(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        FeedUpdater(self.rss_2.id, self.parsed_feed_item).update_feeds()
        self.assertEqual(FeedItem.objects.all().count(), 20)
        self.assertEqual(FeedItem.objects.filter(rss_feed=self.rss_1).count(), 10)
        self.assertEqual(FeedItem.objects.filter(rss_feed=self.rss_2).count(), 10)

    def test_feed_last_try(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        last_try = RSSFeed.objects.get(id=self.rss_1.id).last_try
        self.assertEqual(last_try > (timezone.now() - timedelta(seconds=1)), True)
        self.assertEqual(last_try < (timezone.now() + timedelta(seconds=1)), True)

    def test_feed_item_title_value(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        for item in self.parsed_feed_item:
            self.assertEqual(FeedItem.objects.filter(title=item['title'], rss_feed=self.rss_1).exists(), True)

    def test_feed_item_link_value(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        for item in self.parsed_feed_item:
            self.assertEqual(FeedItem.objects.filter(link=item['link'], rss_feed=self.rss_1).exists(), True)

    def test_feed_item_description_value(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        for item in self.parsed_feed_item:
            self.assertEqual(FeedItem.objects.filter(description=item['summary'], rss_feed=self.rss_1).exists(), True)

    def test_feed_item_author_value(self):
        FeedUpdater(self.rss_1.id, self.parsed_feed_item).update_feeds()
        for item in self.parsed_feed_item:
            self.assertEqual(FeedItem.objects.filter(author=item['author'], rss_feed=self.rss_1).exists(), True)

    def test_read_rss_length(self):
        data = RSSReaderService(self.parsed_feed).read_rss()
        self.assertEqual(len(data), 10)

    def test_read_rss_keys(self):
        data = RSSReaderService(self.parsed_feed).read_rss()[0]
        self.assertEqual('link' in data.keys(), True)
        self.assertEqual('title' in data.keys(), True)
        self.assertEqual('published' in data.keys(), True)
        self.assertEqual('author' in data.keys(), True)
        self.assertEqual('summary' in data.keys(), True)
        self.assertEqual(len(data.keys()), 5)

    def test_read_rss_values(self):
        data = RSSReaderService(self.parsed_feed).read_rss()[0]
        self.assertEqual(data["link"], "https://www.tahghighestan.ir/the-most-popular-apartment-flowers/")
        self.assertEqual(data["title"], 'انواع محبوب ترین گل های آپارتمانی و روش نگهداری آن ها')
        self.assertEqual(data["published"], "Mon, 27 Dec 2021 10:17:26 +0000")
        self.assertEqual(data["author"], 'حسین شریفی')
        self.assertEqual(data["summary"],
                         'انواع محبوب ترین گل های آپارتمانی و روش نگهداری آن ها محبوب ترین گل های آپارتمانی به عنوان پرفروش ترین نمونه های موجود در گل فروشی ها شناخته می شوند. این نمونه ها نیازمند نگهداری صحیح، روش های جدید در این زمینه و &#8230; هستند. برای آن که بتوانید بهترین نمونه های موجود را در [&#8230;]')  # noqa E501

    def test_read_rss_none_values(self):
        data = RSSReaderService(self.parsed_feed).read_rss()[1]
        self.assertEqual(data["title"], None)
