from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication

from digicloud.fetcher.api.filtersets.article import RSSFeedItemFilterSet
from digicloud.fetcher.api.serializers.article import RSSPureItemSerializer
from digicloud.fetcher.models import FeedItem


class FeedItemViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RSSPureItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RSSFeedItemFilterSet
    ordering_fields = ['date', 'rss_feed']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RSSPureItemSerializer
        return super(FeedItemViewSet, self).get_serializer_class()

    def get_queryset(self):
        return FeedItem.objects.all()
