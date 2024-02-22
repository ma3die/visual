from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RegisterView, ProfileViewSet, FollowerViewSet

router = DefaultRouter()
router.register(r'users', AccountViewSet, basename='users')
# router.register(r'me', ProfileViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/reg/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token'),
    path('auth/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('me/', ProfileViewSet.as_view({'get': 'retrive'}), name='profile'),
    path('me/<int:pk>/', ProfileViewSet.as_view({'patch': 'partial_update'}), name='partial_update'),
    path('me/delete/<int:pk>/', ProfileViewSet.as_view({'delete': 'destroy'}), name='destroy'),




    #Follower
    path('subscribe/', FollowerViewSet.as_view({'post': 'subscribe'}), name='subscribted'),
    path('my_subscriptions/<int:follower_id>/', FollowerViewSet.as_view({'get': 'my_subscriptions'}), name='my_subscriptions'),
    path('my_followers/<int:author_id>/', FollowerViewSet.as_view({'get': 'my_followers'}), name='my_followers'),
    # path('reg/', views.,name='register')
]