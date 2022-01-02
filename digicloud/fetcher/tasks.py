from celery import shared_task


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=7, retry_kwargs={'max_retries': 5}, time_limit=60)
def get_new_rss(self, rss_url, rss_id):
    from digicloud.fetcher.services.rss_fetcher import RSSFetcher
    RSSFetcher.fetch_rss(rss_url, rss_id)


@shared_task
def update_rss_items(rss_id, items):
    from digicloud.fetcher.services.feed_updater import FeedUpdater
    FeedUpdater(rss_id, items).update_feeds()


@shared_task
def update_all_rss():
    from digicloud.fetcher.services.update_all_rss import UpdateRSS
    UpdateRSS.update_all_rss()
