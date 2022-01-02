from rest_framework.test import APITestCase
from rest_framework.utils import json

from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status


class TestUserLogoutViewSet(APITestCase):

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

    def test_ok_logout(self):
        r = self.client.post(reverse('api:user:user-login'), {"username": self.complete_user1['email'],
                                                              "password": self.complete_user1['password']})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        headers = {
            "HTTP_AUTHORIZATION": "Token " + r.data['token']
        }

        res = self.client.get(reverse('api:user:user-logout'), **headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        r_tmp = self.client.get(reverse('api:user:user-logout'), **headers)
        self.assertEqual(r_tmp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(json.loads(r_tmp.content), {"detail": "Invalid token."})

    def test_ok_multiple_logout(self):
        res1 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        res2 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        headers1 = {
            "HTTP_AUTHORIZATION": "Token " + res1.data['token']
        }

        headers2 = {
            "HTTP_AUTHORIZATION": "Token " + res2.data['token']
        }

        res = self.client.get(reverse('api:user:user-logout'), **headers1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(reverse('api:user:user-logout'), **headers2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_not_login_logout(self):
        res = self.client.get(reverse('api:user:user-logout'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(json.loads(res.content), {"detail": "Authentication credentials were not provided."})

    def test_ok_logout_all(self):
        res1 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        res2 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        headers1 = {
            "HTTP_AUTHORIZATION": "Token " + res1.data['token']
        }

        headers2 = {
            "HTTP_AUTHORIZATION": "Token " + res2.data['token']
        }

        res = self.client.get(reverse('api:user:user-logout-all'), **headers1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(reverse('api:user:user-logout'), **headers2)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(json.loads(res.content), {"detail": "Invalid token."})

    def test_not_login_logout_all(self):
        res = self.client.get(reverse('api:user:user-logout-all'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(json.loads(res.content), {"detail": "Authentication credentials were not provided."})
