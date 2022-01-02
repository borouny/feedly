from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication

from digicloud.feed_management.api.filtersets.bookmark import UserFeedBookmarkItemFilterSet
from digicloud.feed_management.api.serilalizers.bookmark import UserFeedBookmarkItemSerializer, \
    UpdatableUserFeedBookmarkItemSerializer
from digicloud.feed_management.models import UserFeedBookmarkItem


class UserFeedBookmarkItemViewSet(DestroyModelMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserFeedBookmarkItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFeedBookmarkItemFilterSet
    ordering_fields = ['item__date']

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserFeedBookmarkItemSerializer
        if self.action in ['create']:
            return UpdatableUserFeedBookmarkItemSerializer
        return super(UserFeedBookmarkItemViewSet, self).get_serializer_class()

    def get_queryset(self):
        return UserFeedBookmarkItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **{'user': self.request.user.id}})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data, self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
