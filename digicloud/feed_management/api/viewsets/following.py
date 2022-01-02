from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication

from digicloud.feed_management.api.serilalizers.following import FollowingSerializer, ReadOnlyFollowingSerializer
from digicloud.feed_management.models import FollowedRSSFeed


class UserRssViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = ReadOnlyFollowingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return ReadOnlyFollowingSerializer
        if self.action in ['create']:
            return FollowingSerializer
        return super(UserRssViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **{'user': self.request.user.id}})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data, self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return FollowedRSSFeed.objects.filter(user=self.request.user)
