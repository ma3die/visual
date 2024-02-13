from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RegisterView, ProfileView, FollowerViewSet

# router = DefaultRouter()
# router.register(r'auth', AccountViewSet, basename='auth')

urlpatterns = [
    path('reg/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),

    #Follower
    path('subscribe/', FollowerViewSet.as_view({'post': 'subscribe'}), name='subscribted'),
    path('my_subscriptions/<int:follower_id>/', FollowerViewSet.as_view({'get': 'my_subscriptions'}), name='my_subscriptions'),
    path('my_followers/<int:author_id>/', FollowerViewSet.as_view({'get': 'my_followers'}), name='my_followers'),
    # path('reg/', views.,name='register')
]