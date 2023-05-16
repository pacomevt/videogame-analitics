from django.urls import path
from .views import index, ScraperView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='scraper-index'),
    path('runtask/', ScraperView.as_view(), name='run-task'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)