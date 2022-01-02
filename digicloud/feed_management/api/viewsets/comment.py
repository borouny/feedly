from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from knox.auth import TokenAuthentication
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from digicloud.feed_management.api.filtersets.comment import CommentFilterSet
from digicloud.feed_management.api.serilalizers.comment import CommentSerializer, ReadOnlyCommentSerializer, \
    UpdatableCommentSerializer
from digicloud.feed_management.models import Comment


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CommentFilterSet
    ordering_fields = ['created']

    def initial(self, request, *args, **kwargs):
        super(CommentViewSet, self).initial(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ['create']:
            return CommentSerializer
        if self.action in ['update', 'partial_update']:
            return UpdatableCommentSerializer
        if self.action in ['retrieve', 'list']:
            return ReadOnlyCommentSerializer
        return super(CommentViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'create', 'destroy']:
            return Comment.objects.filter(user=self.request.user, is_active=True)
        if self.action in ['retrieve', 'list']:
            return Comment.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **{'user': self.request.user.id}})
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data, self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
