"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAdminUser

schema_view = get_schema_view(
    openapi.Info(
        title='todo-app',
        default_version='v1',
        terms_of_service='https://www.google.com/policies/terms/',
        license=openapi.License(name='MIT license')
    ),
    public=True,
    permission_classes=[IsAdminUser]
)

# apps & admin path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('message/', include('message.urls', namespace='message')),
    path('private-data/', include('private_data.urls', namespace='private-data'))
]

# api path
urlpatterns += [
    # login and logout by rest_framework
    path('api-auth/', include('rest_framework.urls')),
    # documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc_ui'),
    path('swagger/output.json', schema_view.without_ui(cache_timeout=0), name='schema_json'),
]

# media & static path
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
