from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('games/', include('games.urls')),
    path('scraper/', include('scraper.urls')),
    path('admin/', admin.site.urls),
]
