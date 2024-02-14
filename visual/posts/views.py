from rest_framework import viewsets
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions
from .models import Post, Comment
from .mixins import LikedMixin
from rest_framework.response import Response

class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = Post.objects.create(
            name=serializer.validated_data['name'],
            # tags=serializer.validated_data['tags'],
            text=serializer.validated_data['text'],
            image=serializer.validated_data['image'],
            author=serializer.validated_data['author'],
        )

        return Response({
            'post_id': post.id,
        })

    def retrieve(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.view_count = post.view_count + 1
        post.save(update_fields=['view_count', ])
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=200)

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'post_slug' in self.kwargs:
            post_slug = self.kwargs['post_slug'].lower()
            post = Post.objects.get(slug=post_slug)
            return Comment.objects.filter(post=post)
        else:
            return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)