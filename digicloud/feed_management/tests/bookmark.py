from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from digicloud.feed_management.models import UserFeedBookmarkItem
from digicloud.fetcher.models import FeedItem
from digicloud.utils.factory.article import FeedItemFactory
from digicloud.utils.factory.bookmark import UserFeedBookmarkItemFactory
from digicloud.utils.factory.rss import RSSFeedFactory
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status
from urllib.parse import urlencode


class TestBookmarkViewSet(APITestCase):

    def setUp(self):
        self.complete_user1 = {
            "password": "1234salam",
            "username": 'test2',
            "email": "test@test.test",
            "mobile": "09366403388",
            "first_name": "Mohammad Sadegh",
            "last_name": "Borouny",
        }
        self.user = UserFactory(username=self.complete_user1['username'],
                                password=self.complete_user1['password'],
                                email=self.complete_user1['email'],
                                mobile=self.complete_user1['mobile'],
                                first_name=self.complete_user1['first_name'],
                                last_name=self.complete_user1['last_name'],
                                )
        r = self.client.post(reverse('api:user:user-login'), {"username": self.user.username,
                                                              "password": self.complete_user1['password']})
        self.headers = {
            "HTTP_AUTHORIZATION": "Token " + r.data['token']
        }

    def test_not_authenticated(self):
        res = self.client.get(reverse('api:feed:bookmark-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_bookmark_list(self):
        for _ in range(100):
            UserFeedBookmarkItemFactory(user=self.user)
        res = self.client.get(reverse('api:feed:bookmark-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 100)
        self.assertEqual(len(res.data['results']), 10)

    def test_user_privacy_bookmark_list(self):
        user2 = UserFactory()
        for _ in range(10):
            UserFeedBookmarkItemFactory(user=self.user)
            UserFeedBookmarkItemFactory(user=user2)
        res = self.client.get(reverse('api:feed:bookmark-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)

    def test_filter_based_on_rss_bookmark_list(self):
        rss_1 = RSSFeedFactory()
        rss_2 = RSSFeedFactory()
        for _ in range(10):
            UserFeedBookmarkItemFactory(user=self.user, item=FeedItemFactory(rss_feed=rss_1))
            UserFeedBookmarkItemFactory(user=self.user, item=FeedItemFactory(rss_feed=rss_2))
        res = self.client.get(f"{reverse('api:feed:bookmark-list')}?{urlencode({'rss': rss_1.id})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)
        for result in res.data['results']:
            rss = FeedItem.objects.get(id=result['item_id']).rss_feed
            self.assertEqual(rss, rss_1)

    def test_filter_based_on_start_date_bookmark_list(self):
        rss_1 = RSSFeedFactory()
        for i in range(10):
            UserFeedBookmarkItemFactory(user=self.user, item=FeedItemFactory(rss_feed=rss_1,
                                                                             date=timezone.now() - timedelta(days=i)))
        start_date = timezone.now() - timedelta(days=5)
        res = self.client.get(f"{reverse('api:feed:bookmark-list')}?{urlencode({'start_date': str(start_date)})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 5)
        self.assertEqual(len(res.data['results']), 5)
        for result in res.data['results']:
            item = FeedItem.objects.get(id=result['item_id'])
            self.assertEqual(item.date > start_date, True)

    def test_filter_based_on_end_date_bookmark_list(self):
        rss_1 = RSSFeedFactory()
        for i in range(10):
            UserFeedBookmarkItemFactory(user=self.user, item=FeedItemFactory(rss_feed=rss_1,
                                                                             date=timezone.now() - timedelta(days=i)))
        end_date = timezone.now() - timedelta(days=5)
        res = self.client.get(f"{reverse('api:feed:bookmark-list')}?{urlencode({'end_date': str(end_date)})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 5)
        self.assertEqual(len(res.data['results']), 5)
        for result in res.data['results']:
            item = FeedItem.objects.get(id=result['item_id'])
            self.assertEqual(item.date < end_date, True)

    def test_date_order_bookmark_list(self):
        rss_1 = RSSFeedFactory()
        for i in range(10):
            UserFeedBookmarkItemFactory(user=self.user, item=FeedItemFactory(rss_feed=rss_1,
                                                                             date=timezone.now() - timedelta(days=i)))
        res = self.client.get(f"{reverse('api:feed:bookmark-list')}?{urlencode({'ordering': 'item__date'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            item_1 = FeedItem.objects.get(id=res.data['results'][i]['item_id'])
            item_2 = FeedItem.objects.get(id=res.data['results'][i + 1]['item_id'])
            self.assertEqual(item_1.date <= item_2.date, True)

    def test_add_bookmark(self):

        item = FeedItemFactory()
        res = self.client.post(reverse('api:feed:bookmark-list'), data={'item': item.id}, format='json',
                               **self.headers)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserFeedBookmarkItem.objects.filter(item=item, user=self.user).exists(), True)

    def test_ignore_multiple_add_bookmark(self):

        item = FeedItemFactory()
        res_1 = self.client.post(reverse('api:feed:bookmark-list'), data={'item': item.id}, format='json',
                                 **self.headers)

        res_2 = self.client.post(reverse('api:feed:bookmark-list'), data={'item': item.id}, format='json',
                                 **self.headers)
        self.assertEqual(res_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserFeedBookmarkItem.objects.filter(item=item, user=self.user).count(), 1)

    def test_delete_bookmark(self):
        item = FeedItemFactory()
        bookmark = UserFeedBookmarkItemFactory(user=self.user, item=item)
        res = self.client.delete(reverse('api:feed:bookmark-detail', kwargs={'pk': bookmark.id}),
                                 **self.headers)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserFeedBookmarkItem.objects.filter(item=item, user=self.user).count(), 0)

    def test_multiple_delete_bookmark(self):
        item = FeedItemFactory()
        bookmark = UserFeedBookmarkItemFactory(user=self.user, item=item)
        res_1 = self.client.delete(reverse('api:feed:bookmark-detail', kwargs={'pk': bookmark.id}),
                                   **self.headers)
        res_2 = self.client.delete(reverse('api:feed:bookmark-detail', kwargs={'pk': bookmark.id}),
                                   **self.headers)
        self.assertEqual(res_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res_2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(UserFeedBookmarkItem.objects.filter(item=item, user=self.user).count(), 0)
