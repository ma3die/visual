from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('notifications/', NotificationView.as_view({'get': 'count_notification'}), name='count_notification'),
    path('notifications/push/', NotificationView.as_view({'get': 'push'}), name='push'),
    path('notifications/list/', NotificationView.as_view({'get': 'list'}), name='list'),
    # path('my_subscriptions/<int:follower_id>/', FollowerViewSet.as_view({'get': 'my_subscriptions'}), name='my_subscriptions'),
    # path('my_followers/<int:author_id>/', FollowerViewSet.as_view({'get': 'my_followers'}), name='my_followers'),
]