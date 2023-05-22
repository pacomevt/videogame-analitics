from django.urls import path
from .views import index, register, logout_user, login_user

urlpatterns = [
    path('', index, name='users-index'),
    path('register/', register, name='users-register'),
    path('login/', login_user, name='users-login'),
    path('logout/', logout_user, name='users-logout'),
    path('profile/', index, name='users-proffile'),
]