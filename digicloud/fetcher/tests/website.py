from rest_framework.test import APITestCase

from digicloud.fetcher.models import Category, RSSFeed
from digicloud.utils.factory.rss import RSSFeedFactory
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status
from urllib.parse import urlencode


class TestWebsiteViewSet(APITestCase):

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

    def test_not_authenticated(self):
        res = self.client.get(reverse('api:rss:website-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_website_rss_list(self):
        for _ in range(100):
            RSSFeedFactory()
        res = self.client.get(reverse('api:rss:website-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 100)
        self.assertEqual(len(res.data['results']), 10)

    def test_filter_based_on_category_list(self):
        for _ in range(10):
            RSSFeedFactory(category=Category.tech.value)
            RSSFeedFactory(category=Category.science.value)
        res = self.client.get(f"{reverse('api:rss:website-list')}?{urlencode({'category': Category.science.value})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)
        for result in res.data['results']:
            self.assertEqual(result['category'], Category.science.value)

    def test_filter_based_on_url_list(self):
        rss_1 = RSSFeedFactory()
        res = self.client.get(f"{reverse('api:rss:website-list')}?{urlencode({'url': rss_1.url})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(len(res.data['results']), 1)
        for result in res.data['results']:
            self.assertEqual(result['url'], rss_1.url)

    def test_filter_based_on_name_list(self):
        rss_1 = RSSFeedFactory()
        res = self.client.get(f"{reverse('api:rss:website-list')}?{urlencode({'name': rss_1.name})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(len(res.data['results']), 1)
        for result in res.data['results']:
            self.assertEqual(result['name'], rss_1.name)

    def test_created_order_website_list(self):
        for _ in range(10):
            RSSFeedFactory()
        res = self.client.get(f"{reverse('api:rss:website-list')}?{urlencode({'ordering': 'created'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            r1 = RSSFeed.objects.get(id=res.data['results'][i]['id'])
            r2 = RSSFeed.objects.get(id=res.data['results'][i + 1]['id'])
            self.assertEqual(r1.created <= r2.created, True)

    def test_name_order_item_list(self):
        for _ in range(10):
            RSSFeedFactory()
        res = self.client.get(f"{reverse('api:rss:website-list')}?{urlencode({'ordering': 'name'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            self.assertEqual(res.data['results'][i]['name'] <= res.data['results'][i + 1]['name'], True)

    def test_retrieve_website(self):
        rss = RSSFeedFactory()
        res = self.client.get(reverse('api:rss:website-detail', kwargs={"pk": rss.id}),
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['url'], rss.url)
        self.assertEqual(res.data['name'], rss.name)
        self.assertEqual(res.data['feed_version'], rss.feed_version)
        self.assertEqual(res.data['category'], rss.category)

    def test_not_find_retrieve_item(self):
        rss = RSSFeedFactory()
        res = self.client.get(reverse('api:rss:website-detail', kwargs={"pk": rss.id + 100}),
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
