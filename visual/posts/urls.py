from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router1 = DefaultRouter()
router1.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router1.urls))
]