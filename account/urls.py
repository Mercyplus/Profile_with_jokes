from django.urls import path, include
from . import views
from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()
router.register(r'Profile', ProfileViewSet)
router.register(r'Jokes', JokesViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('signout/', views.signoutView, name='signout'),
    path('edit/', views.edit, name='edit'),
    path('api/', include(router.urls)),
]
