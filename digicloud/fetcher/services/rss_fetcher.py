import feedparser
from digicloud.fetcher.services.rss_reader import RSSReaderService
from digicloud.fetcher.tasks import update_rss_items


class RSSFetcher:
    @staticmethod
    def fetch_rss(rss_url, rss_id):
        parsed_rss = feedparser.parse(rss_url)
        if len(parsed_rss.get('entries', [])) == 0:
            raise Exception
        items = RSSReaderService(parsed_rss).read_rss()
        update_rss_items.apply_async(
            args=(rss_id, items),
            queue='update_rss_item'
        )
