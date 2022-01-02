from digicloud.fetcher.models import RSSFeed
from digicloud.fetcher.tasks import get_new_rss


class UpdateRSS:
    @staticmethod
    def update_all_rss():
        rss_list = RSSFeed.objects.filter(is_active=True)
        for rss in rss_list:
            get_new_rss.apply_async(
                args=(rss.url, rss.id),
                queue='rss_fetcher'
            )
