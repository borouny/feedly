"""digicloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls import include, url

from digicloud.feed_management.api.router import feed_management_api_urlpatterns
from digicloud.fetcher.api.router import item_api_urlpatterns
from digicloud.user_management.api.router import user_management_api_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Digi Cloud Task API",
        default_version='v1',
        description="Digi Cloud Task API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="borouny@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    url=f'{settings.HOST_BASE_URL}/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    url(r'^accounts/', include((user_management_api_urlpatterns, 'user'))),
    url(r'^feeds/', include((feed_management_api_urlpatterns, 'feed'))),
    url(r'^rss/', include((item_api_urlpatterns, 'rss'))),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include((api_urlpatterns, 'api'))),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
