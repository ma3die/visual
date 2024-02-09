from rest_framework import viewsets
from .serializers import PostSerializer
from rest_framework import permissions
from .models import Post
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = Post.objects.create(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
        )

        return Response({
            'user_id': user.id,
        })