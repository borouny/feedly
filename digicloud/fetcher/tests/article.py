from rest_framework.test import APITestCase
from digicloud.utils.factory.article import FeedItemFactory
from digicloud.utils.factory.rss import RSSFeedFactory
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status
from urllib.parse import urlencode


class TestArticleViewSet(APITestCase):

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
        r = self.client.post(reverse('api:user:user-login'), {"username": self.complete_user1['email'],
                                                              "password": self.complete_user1['password']})
        self.headers = {
            "HTTP_AUTHORIZATION": "Token " + r.data['token']
        }
        self.rss = RSSFeedFactory()

    def test_not_authenticated(self):
        res = self.client.get(reverse('api:rss:items-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_item_list(self):
        for _ in range(100):
            FeedItemFactory(rss_feed=self.rss)
        res = self.client.get(reverse('api:rss:items-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 100)
        self.assertEqual(len(res.data['results']), 10)
        self.assertEqual(res.data['results'][0]['rss_feed'], self.rss.id)

    def test_filter_based_on_rss_item_list(self):
        rss_2 = RSSFeedFactory()
        for _ in range(10):
            FeedItemFactory(rss_feed=self.rss)
            FeedItemFactory(rss_feed=rss_2)
        res = self.client.get(f"{reverse('api:rss:items-list')}?{urlencode({'rss_feed': self.rss.id})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)
        for result in res.data['results']:
            self.assertEqual(result['rss_feed'], self.rss.id)

    def test_date_order_item_list(self):
        for _ in range(10):
            FeedItemFactory(rss_feed=self.rss)
        res = self.client.get(f"{reverse('api:rss:items-list')}?{urlencode({'ordering': 'date'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            self.assertEqual(res.data['results'][i]['date'] >= res.data['results'][i + 1]['date'], True)

    def test_rss_feed_order_item_list(self):
        rss_2 = RSSFeedFactory()
        for _ in range(5):
            FeedItemFactory(rss_feed=self.rss)
            FeedItemFactory(rss_feed=rss_2)
        res = self.client.get(f"{reverse('api:rss:items-list')}?{urlencode({'ordering': 'rss_feed'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            self.assertEqual(res.data['results'][i]['rss_feed'] <= res.data['results'][i + 1]['rss_feed'], True)

    def test_retrieve_item(self):
        item = FeedItemFactory(rss_feed=self.rss)
        res = self.client.get(reverse('api:rss:items-detail', kwargs={"pk": item.id}),
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['rss_feed'], self.rss.id)
        self.assertEqual(res.data['link'], item.link)
        self.assertEqual(res.data['title'], item.title)
        self.assertEqual(res.data['description'], item.description)
        self.assertEqual(res.data['author'], item.author)

    def test_not_find_retrieve_item(self):
        item = FeedItemFactory(rss_feed=self.rss)
        res = self.client.get(reverse('api:rss:items-detail', kwargs={"pk": item.id + 100}),
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
