from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import user_logged_out, authenticate

from digicloud.user_management.api.serializers import CreateUserSerializer, LoginUserSerializer
import logging

logger = logging.getLogger(__name__)


class UserViewSet(GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = []

    def get_permissions(self):
        if self.action in ['logout', 'logout_all']:
            return [IsAuthenticated()]
        if self.action in ['login', 'register']:
            return [AllowAny()]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginUserSerializer
        if self.action == 'register':
            return CreateUserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data, request=request)
        if not user:
            return Response({
                "errors": [{
                    "messages": [_("Sorry, that username or password isn't right.")]
                }]
            }, status=status.HTTP_403_FORBIDDEN)
        token = AuthToken.objects.create(user)[1]
        return Response({
            "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response({"message": _("User Logged out successfully")}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def logout_all(self, request):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response({"message": _("User Logged out from all his sessions successfully")}, status=status.HTTP_200_OK)
