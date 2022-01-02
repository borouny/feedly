from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication

from digicloud.fetcher.api.filtersets.website import RSSFeedFilterSet
from digicloud.fetcher.api.serializers.website import RSSSerializer
from digicloud.fetcher.models import RSSFeed


class WebsiteViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RSSSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RSSFeedFilterSet
    ordering_fields = ['name', 'created', 'last_try']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RSSSerializer
        return super(WebsiteViewSet, self).get_serializer_class()

    def get_queryset(self):
        return RSSFeed.objects.all()
