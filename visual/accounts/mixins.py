from rest_framework.decorators import action
from rest_framework.response import Response
from . import services
from posts.serializers import ListPostSerializer


class UserPostMixin:
    """Миксин для получения своей страницы пользователя"""
    @action(detail=True, methods=['GET'])
    def my_posts(self, request, pk=None):
        user = self.get_object()
        posts = services.my_post(user)
        serializer = ListPostSerializer(instance=posts, many=True)
        return Response(serializer.data)


