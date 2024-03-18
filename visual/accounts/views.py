from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsUserProfile
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from .models import Account
from posts.models import Comment
from .serializers import AccountSerializer, RegisterSerializer
from .mixins import UserPostMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class AccountViewSet(UserPostMixin, viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['my_posts']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        try:
            user = get_object_or_404(queryset, pk=pk)
        except:
            raise NotFound
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': AccountSerializer(user, context=self.get_serializer()).data,
            'message': 'Пользователь успешно создан',
        })


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """
    Профиль пользователя
    """
    permission_classes = [IsUserProfile]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def retrive(self, request):
        """
        Данные пользователя
        """
        serializer = AccountSerializer(instance=request.user)
        return Response({
            'user': serializer.data
        })

    def perform_destroy(self, instance):
        deleted_user = Account.objects.get(username='deleted')
        user_id = instance.id
        all_user_comment = Comment.objects.filter(author_id=user_id)
        for comment in all_user_comment:
            comment.author_id = deleted_user.id
            comment.save()
        instance.delete()
    # def partial_update(self, request, author_id):
    #     """
    #     Изменить данные пользователя
    #     """
    #     serializer = ProfileSerializer(instance=request.user, data=request.data, partial=True)
    #     serializer.is_valid()
    #     serializer.save()
    #     return Response(serializer.data)
    # @action(detail=True, methods=['DELETE'])
    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)



