from rest_framework.test import APITestCase
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from digicloud.user_management.models import User
from rest_framework import status


class TestUserLoginViewSet(APITestCase):

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

    def test_login_by_email(self):
        res = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                'password': self.complete_user1['password']})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertDictEqual(res.data['user'], {
            'id': 1,
            'first_name': self.complete_user1.get('first_name', ''),
            'last_name': self.complete_user1.get('last_name', ''),
            'mobile': self.complete_user1['mobile'],
            'email': self.complete_user1['email'],
            'username': self.complete_user1['username'],
        })

    def test_ok_login(self):
        res = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                'password': self.complete_user1['password']})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data['user'], {
            'id': 1,
            'first_name': self.complete_user1.get('first_name', ''),
            'last_name': self.complete_user1.get('last_name', ''),
            'mobile': self.complete_user1['mobile'],
            'email': self.complete_user1['email'],
            'username': self.complete_user1['username'],
        })
        self.assertIn('token', res.data)
        u = User.objects.get(username=self.complete_user1['username'])
        self.assertTrue(u.is_authenticated)

    def test_multiple_login(self):
        res1 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        res2 = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                 'password': self.complete_user1['password']})
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in res1.data)
        self.assertTrue('token' in res2.data)
        self.assertNotEqual(res1.data['token'], res2.data['token'])

    def test_wrong_password_login(self):
        res = self.client.post(reverse('api:user:user-login'), {'username': self.complete_user1['email'],
                                                                'password': "wrong pass"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(res.data, {
            "errors": [{
                'messages': ["Sorry, that username or password isn't right."]
            }]
        })

    def test_wrong_username_and_email_login(self):
        res = self.client.post(reverse('api:user:user-login'), {'username': "sadegh@sadegh.sadegh",
                                                                'password': "test"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(res.data, {
            "errors": [{
                'messages': ["Sorry, that username or password isn't right."]
            }]
        })
