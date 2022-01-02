from rest_framework.routers import DefaultRouter

from digicloud.feed_management.api.viewsets.comment import CommentViewSet
from digicloud.feed_management.api.viewsets.bookmark import UserFeedBookmarkItemViewSet
from digicloud.feed_management.api.viewsets.following import UserRssViewSet

app_name = 'feed_management'

feed_management_router = DefaultRouter()
feed_management_router.register(r'following', UserRssViewSet, 'following')
feed_management_router.register(r'bookmark', UserFeedBookmarkItemViewSet, 'bookmark')
feed_management_router.register(r'comments', CommentViewSet, 'comment')

feed_management_api_urlpatterns = feed_management_router.urls
