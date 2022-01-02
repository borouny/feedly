from rest_framework.test import APITestCase

from digicloud.feed_management.models import FollowedRSSFeed
from digicloud.utils.factory.following import FollowedRSSFeedFactory
from digicloud.utils.factory.rss import RSSFeedFactory
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status


class TestFollowingViewSet(APITestCase):

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
        res = self.client.get(reverse('api:feed:following-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_following_list(self):
        for _ in range(100):
            FollowedRSSFeedFactory(user=self.user)
        res = self.client.get(reverse('api:feed:following-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 100)
        self.assertEqual(len(res.data['results']), 10)

    def test_user_privacy_following_list(self):
        user2 = UserFactory()
        for _ in range(10):
            FollowedRSSFeedFactory(user=self.user)
            FollowedRSSFeedFactory(user=user2)
        res = self.client.get(reverse('api:feed:following-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)

    def test_add_following(self):
        rss = RSSFeedFactory()
        res = self.client.post(reverse('api:feed:following-list'), data={'rss_feed': rss.id}, format='json',
                               **self.headers)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FollowedRSSFeed.objects.filter(rss_feed=rss, user=self.user).exists(), True)

    def test_ignore_multiple_add_following(self):

        rss = RSSFeedFactory()
        res_1 = self.client.post(reverse('api:feed:following-list'), data={'rss_feed': rss.id}, format='json',
                                 **self.headers)
        res_2 = self.client.post(reverse('api:feed:following-list'), data={'rss_feed': rss.id}, format='json',
                                 **self.headers)
        self.assertEqual(res_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FollowedRSSFeed.objects.filter(rss_feed=rss, user=self.user).count(), 1)

    def test_unfollow(self):
        rss = RSSFeedFactory()
        following = FollowedRSSFeedFactory(user=self.user, rss_feed=rss)
        res = self.client.delete(reverse('api:feed:following-detail', kwargs={'pk': following.id}),
                                 **self.headers)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FollowedRSSFeed.objects.filter(rss_feed=rss, user=self.user).count(), 0)

    def test_multiple_unfollow(self):
        rss = RSSFeedFactory()
        following = FollowedRSSFeedFactory(user=self.user, rss_feed=rss)
        res_1 = self.client.delete(reverse('api:feed:following-detail', kwargs={'pk': following.id}),
                                   **self.headers)
        res_2 = self.client.delete(reverse('api:feed:following-detail', kwargs={'pk': following.id}),
                                   **self.headers)
        self.assertEqual(res_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res_2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(FollowedRSSFeed.objects.filter(rss_feed=rss, user=self.user).count(), 0)
