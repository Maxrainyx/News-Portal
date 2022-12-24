
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include(('News.urls', 'News'), namespace='news')),
    path('articles/', include('News.urls')),
    path('sign/', include('sign.urls')),
    path('', include('protect.urls')),
    path('accounts/', include('allauth.urls')),
]
