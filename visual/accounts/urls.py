from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RegisterView, ProfileView

# router = DefaultRouter()
# router.register(r'auth', AccountViewSet, basename='auth')

urlpatterns = [
    path('reg/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token')
    # path('reg/', views.,name='register')
]