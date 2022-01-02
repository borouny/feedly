from rest_framework.routers import DefaultRouter
from digicloud.user_management.api.viewsets import UserViewSet

app_name = 'user_management'

user_management_router = DefaultRouter()
user_management_router.register(r'', UserViewSet, 'user')

user_management_api_urlpatterns = user_management_router.urls
