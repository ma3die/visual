from rest_framework import viewsets
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, CreateCommentSerializer, ListPostSerializer
from accounts.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthorComment
from rest_framework import permissions
from .models import Post, Comment
from accounts.models import Follower
from accounts.serializers import FollowerSerializer
from .mixins import LikedMixin
from rest_framework.response import Response


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action in ['likes']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['like', 'unlike']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = request.user
        if user.is_authenticated:
            ids = []
            subscripted = Follower.objects.filter(follower_id=user.id)
            serializer = FollowerSerializer(subscripted, many=True)
            querys = serializer.data
            for query in querys:
                id = query['author']
                ids.append(id)
            queryset = Post.objects.filter(author_id__in=ids)[:10]
        else:
            queryset = Post.objects.all()
        serializer = ListPostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.view_count = post.view_count + 1
        post.save(update_fields=['view_count', ])
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=200)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """CRUD комментарии"""
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthorComment]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
