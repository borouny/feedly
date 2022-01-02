from rest_framework.routers import DefaultRouter

from digicloud.fetcher.api.viewsets.artticle import FeedItemViewSet
from digicloud.fetcher.api.viewsets.website import WebsiteViewSet

app_name = 'feed_management'

item_router = DefaultRouter()
item_router.register(r'items', FeedItemViewSet, 'items')
item_router.register(r'websites', WebsiteViewSet, 'website')

item_api_urlpatterns = item_router.urls
