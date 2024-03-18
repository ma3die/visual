from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowerViewSet


urlpatterns = [
    path('subscribe/', FollowerViewSet.as_view({'post': 'subscribe'}), name='subscribted'),
    path('my_subscriptions/<int:follower_id>/', FollowerViewSet.as_view({'get': 'my_subscriptions'}), name='my_subscriptions'),
    path('my_followers/<int:author_id>/', FollowerViewSet.as_view({'get': 'my_followers'}), name='my_followers'),
]