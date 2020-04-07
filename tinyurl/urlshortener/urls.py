from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'urlshortener'


urlpatterns = [
    path('', views.urlshortener, name='urlshortener'),
    path('<str:shorturl>', views.get_shorturl, name='shorturl'),
]

if 'rest_framework' in settings.INSTALLED_APPS:
    router = routers.DefaultRouter()
    router.register('api/tinyurl', views.UrlShortenerViewSet)
    urlpatterns += path('', include(router.urls)),
    urlpatterns += path('api/auth/', include('rest_framework.urls')),
    
