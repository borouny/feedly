from rest_framework.test import APITestCase
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from digicloud.user_management.models import User
from rest_framework import status

import copy
import json


class TestUserRegisterViewSet(APITestCase):

    def setUp(self):
        self.complete_user1 = {
            "password": "1234salam",
            "username": 'test2',
            "email": "test@test.test",
        }

    def test_register_invalid_email(self):
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info['email'] = 'fdsfdsf'
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertDictEqual(json.loads(res.content), {"email": ["Enter a valid email address."]})

    def test_register_no_email(self):
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info.pop('email')
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertDictEqual(json.loads(res.content), {"email": ["This field is required."]})

    def test_register_no_username(self):
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info.pop('username')
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertDictEqual(json.loads(res.content), {"username": ["This field is required."]})

    def test_register_no_password(self):
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info.pop('password')
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertDictEqual(json.loads(res.content), {"password": ["This field is required."]})

    def test_register_weak_password(self):
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info['password'] = '1234'
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertDictEqual(json.loads(res.content), {"password": ["Password is not Strong Enough."]})

    def test_register_ok(self):
        res = self.client.post(reverse('api:user:user-register'), self.complete_user1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.all()), 1)

    def test_register_same_email(self):
        user2 = UserFactory()
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info['email'] = user2.email
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertDictEqual(json.loads(res.content), {"email": ["An account already exists with this email"]})

    def test_register_same_username(self):
        user2 = UserFactory()
        bad_info = copy.deepcopy(self.complete_user1)
        bad_info['username'] = user2.username
        res = self.client.post(reverse('api:user:user-register'), bad_info)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertDictEqual(json.loads(res.content), {"username": ["A user with that username already exists."]})
