from rest_framework import viewsets
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, CreateCommentSerializer, ListPostSerializer
    # , PostDetailSerializer
from accounts.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthorComment
from rest_framework import permissions
from .models import Post, Comment
from accounts.models import Follower
from accounts.serializers import FollowerSerializer
from .mixins import LikedMixin
from rest_framework.response import Response


# class PostDetailView(generics.RetrieveAPIView):
#     """Вывод полной статьи"""
#     permission_classes = [permissions.AllowAny]
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = "pk"

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
            subscripted = Follower.objects.filter(follower_id=user.id)
            serializers = FollowerSerializer(subscripted, many=True)
        queryset = Post.objects.all()
        permission_classes = [permissions.AllowAny]
        serializer = ListPostSerializer(queryset, many=True)
        return Response(serializer.data)
    # def perform_create(self, serializer):
    #     post = 3
    #     tag = serializer.validated_data['tags']
    #     instance = serializer.save()
    #     if 'tags' in self.request.data:
    #         instance.tags.set(*self.request.data['tags'])
    #         post = 2

    # def create(self, request):
    #     serializer = PostSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     post = Post.objects.create(
    #         name=serializer.validated_data['name'],
    #         tags=serializer.validated_data['tags'],
    #         text=serializer.validated_data['text'],
    #         image=serializer.validated_data['image'],
    #         author=serializer.validated_data['author'],
    #     )
    #
    #     return Response({
    #         'post_id': post.id,
    #     })

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

    # def get_queryset(self):
    #     if 'post_slug' in self.kwargs:
    #         post_slug = self.kwargs['post_slug'].lower()
    #         post = Post.objects.get(slug=post_slug)
    #         return Comment.objects.filter(post=post)
    #     else:
    #         return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()