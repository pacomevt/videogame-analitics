from django.urls import path
from .views import index, game_detail
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='games-index'),
    path('<slug:slug>', game_detail, name='game-detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)