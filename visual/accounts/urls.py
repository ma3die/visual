from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RegisterView, ProfileViewSet, CreatePaymentView,\
    CreatePaymentAcceptedView, UserConfirmEmailView, VKLoginRedirectView, VKLoginView, GoogleLoginRedirectView

router = DefaultRouter()
router.register(r'users', AccountViewSet, basename='users')
# router.register(r'me', ProfileViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/reg/', RegisterView.as_view(), name='register'),
    path('auth/reg/callback/', VKLoginView.as_view(), name='callback'),
    path('auth/reg/redirect/', VKLoginRedirectView.as_view(), name='redirect'),
    path('auth/reg/callback_google/', VKLoginView.as_view(), name='callback_google'),
    path('auth/reg/redirect_google/', GoogleLoginRedirectView.as_view(), name='redirect_google'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token'),
    path('auth/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('me/', ProfileViewSet.as_view({'get': 'retrive'}), name='profile'),
    path('me/<int:pk>/', ProfileViewSet.as_view({'patch': 'partial_update'}), name='partial_update'),
    path('me/delete/<int:pk>/', ProfileViewSet.as_view({'delete': 'destroy'}), name='destroy'),
    path('create_payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('accepted_payment/', CreatePaymentAcceptedView.as_view(), name='create_payment'),
]