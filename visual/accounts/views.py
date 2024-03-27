import uuid
import json
from yookassa import Configuration, Payment

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.shortcuts import get_object_or_404

from posts.models import Comment, Post
from .models import Account
from .mixins import UserPostMixin
from .permissions import IsUserProfile
from .serializers import AccountSerializer, RegisterSerializer

Configuration.account_id = '357017'
Configuration.secret_key = 'test_okbLKMNPtyaarXd2dH8sAicWQdi_Ok_hifBC2z4mKVg'

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

class CreatePaymentView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer
    def post(self, request):
        user = request.user
        subscription = request.data.get('subscription')
        value = request.data.get('value')

        payment = Payment.create({
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/api/me/"
            },
            "metadata": {
                "user_id": user.id,
                "subscription": subscription
            },
            "capture": True,
            "test": True,
            "description": "Заказ №1"
        }, uuid.uuid4())
        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url
        return Response({'confirmation_url': confirmation_url})


class CreatePaymentAcceotedView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        response = request.data.get('payment_id')
        user_id = request.data.get('user_id')
        subscription = request.data.get('subscription')

        payment = Payment.find_one(response)
        if payment.status == 'succeeded':
            if subscription:
                user = Account.objects.get(id=user_id)
                user.subscription = subscription
                if subscription == 'premium':
                    posts = Post.objects.filter(author_id=user_id)
                    posts.update(premium=True)
                    return Response(400)

        else:
            return Response(400)


