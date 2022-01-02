from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase

from digicloud.feed_management.models import Comment
from digicloud.utils.factory.article import FeedItemFactory
from digicloud.utils.factory.comment import CommentFactory
from digicloud.utils.factory.user import UserFactory
from django.urls import reverse
from rest_framework import status
from urllib.parse import urlencode


class TestCommentViewSet(APITestCase):

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
        res = self.client.get(reverse('api:feed:comment-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_commentk_list(self):
        for _ in range(100):
            CommentFactory(user=self.user)
        res = self.client.get(reverse('api:feed:comment-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 100)
        self.assertEqual(len(res.data['results']), 10)

    def test_user_see_all_comment_list(self):
        user2 = UserFactory()
        for _ in range(10):
            CommentFactory(user=self.user)
            CommentFactory(user=user2)
        res = self.client.get(reverse('api:feed:comment-list'), **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 20)
        self.assertEqual(len(res.data['results']), 10)

    def test_filter_based_on_user_comment_list(self):
        item_1 = FeedItemFactory()
        item_2 = FeedItemFactory()
        user_2 = UserFactory()
        for _ in range(10):
            CommentFactory(user=self.user, feed_item=item_1)
            CommentFactory(user=user_2, feed_item=item_2)
        res = self.client.get(f"{reverse('api:feed:comment-list')}?{urlencode({'user': self.user.id})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)
        for result in res.data['results']:
            self.assertEqual(result["user"], self.user.id)

    def test_filter_based_on_item_comment_list(self):
        item_1 = FeedItemFactory()
        item_2 = FeedItemFactory()
        user_2 = UserFactory()
        for _ in range(10):
            CommentFactory(user=self.user, feed_item=item_1)
            CommentFactory(user=user_2, feed_item=item_2)
        res = self.client.get(f"{reverse('api:feed:comment-list')}?{urlencode({'feed_item': item_1.id})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 10)
        self.assertEqual(len(res.data['results']), 10)
        for result in res.data['results']:
            self.assertEqual(result["feed_item"], item_1.id)

    def test_created_order_comment_list(self):
        item_1 = FeedItemFactory()
        for i in range(10):
            CommentFactory(user=self.user, feed_item=item_1, created=timezone.now() - timedelta(days=i))
        res = self.client.get(f"{reverse('api:feed:comment-list')}?{urlencode({'ordering': 'created'})}",
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in range(0, 9, 1):
            self.assertEqual(res.data['results'][i]['created'] <= res.data['results'][i + 1]['created'], True)

    def test_add_comment(self):
        item = FeedItemFactory()
        res = self.client.post(reverse('api:feed:comment-list'), data={'feed_item': item.id,
                                                                       'title': "title",
                                                                       'description': 'description'
                                                                       },
                               format='json',
                               **self.headers)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Comment.objects.filter(feed_item=item, user=self.user, title='title', description="description").exists(),
            True)

    def test_update_comment(self):
        comment = CommentFactory(user=self.user)
        res = self.client.put(reverse('api:feed:comment-detail', kwargs={"pk": comment.id}),
                              data={'title': "new title",
                                    'description': 'new description'},
                              format='json',
                              **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comment.objects.filter(user=self.user, id=comment.id, title='new title',
                                   description="new description").exists(),
            True)

    def test_partial_update_title_comment(self):
        comment = CommentFactory(user=self.user)
        res = self.client.patch(reverse('api:feed:comment-detail', kwargs={"pk": comment.id}),
                                data={'title': "new title"},
                                format='json',
                                **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comment.objects.filter(user=self.user, id=comment.id, description=comment.description,
                                   title="new title").exists(),
            True)

    def test_partial_update_description_comment(self):
        comment = CommentFactory(user=self.user)
        res = self.client.patch(reverse('api:feed:comment-detail', kwargs={"pk": comment.id}),
                                data={'description': "new description"},
                                format='json',
                                **self.headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comment.objects.filter(user=self.user, id=comment.id, title=comment.title,
                                   description="new description").exists(),
            True)

    def test_delete_comment(self):
        comment = CommentFactory(user=self.user)
        res = self.client.delete(reverse('api:feed:comment-detail', kwargs={'pk': comment.id}),
                                 **self.headers)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.get(id=comment.id).is_active, False)

    def test_multiple_delete_bookmark(self):
        comment = CommentFactory(user=self.user)
        res_1 = self.client.delete(reverse('api:feed:comment-detail', kwargs={'pk': comment.id}),
                                   **self.headers)
        res_2 = self.client.delete(reverse('api:feed:comment-detail', kwargs={'pk': comment.id}),
                                   **self.headers)
        self.assertEqual(res_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res_2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.get(id=comment.id).is_active, False)
