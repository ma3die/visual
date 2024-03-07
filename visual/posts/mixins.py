from rest_framework.decorators import action
from rest_framework.response import Response
from . import services
from .models import Image, Video
from .serializers import LikeSerializer, ImageSerializer, VideoSerializer


class LikedMixin:

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        """Лайк"""
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['post'])
    def unlike(self, request, slug=None):
        """Удалить лайк"""
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['get'])
    def likes(self, request, slug=None):
        """Получает всех пользователей, которые лайкнули post"""
        obj = self.get_object()
        user = services.get_likes(obj)
        serializer = LikeSerializer(user, many=True)
        return Response(serializer.data)


class AddImageVideoMixin:
    def add_image(self, file, post_id):
        image_data = {}
        image_data['image'] = file
        image_data['post'] = post_id
        serializer_image = ImageSerializer(data=image_data)
        serializer_image.is_valid(raise_exception=True)
        Image.objects.create(**serializer_image.validated_data)

    def choose_add(self, type, file, post_id):
        if type == 'image':
            self.add_image(file, post_id)