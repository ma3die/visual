from rest_framework.decorators import action
from rest_framework.response import Response
from . import services
from .serializers import LikeSerializer


class LikedMixin:

    @action(detail=True, methods=['post'])
    def like(self, request, slug=None):
        '''Лайк'''
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['post'])
    def unlike(self, request, slug=None):
        '''Удалить лайк'''
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['get'])
    def likes(self, request, slug=None):
        '''Получает всех пользователей, которые лайкнули post'''
        obj = self.get_object()
        user = services.get_likes(obj)
        serializer = LikeSerializer(user, many=True)
        return Response(serializer.data)