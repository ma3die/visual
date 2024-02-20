from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CommentView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', CommentView.as_view()),
    # path('comments/<slug:post_slug>/', CommentView.as_view()),
    path('comments/<int:pk>/', CommentView.as_view()),
    # path('posts/<int:pk>/', PostDetailView.as_view())
]