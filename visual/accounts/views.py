import uuid
import json
from yookassa import Configuration, Payment
import logging
import jwt
from jwt import decode as jwt_decode
from urllib.parse import parse_qs
from attrs import define
import requests

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


from django.shortcuts import get_object_or_404, redirect

from posts.models import Comment, Post
from .models import Account
from .mixins import UserPostMixin
from .permissions import IsUserProfile
from .serializers import AccountSerializer, RegisterSerializer
from.services import VKLoginService, get_tokens_for_user

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login


Configuration.account_id = '357017'
Configuration.secret_key = 'test_okbLKMNPtyaarXd2dH8sAicWQdi_Ok_hifBC2z4mKVg'


logger = logging.getLogger('django')

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
            logger.info(f'Login user | {self.request.user.username}')
        except:
            raise NotFound
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        logger.info(f'Post data try | {request.data}')
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': AccountSerializer(user, context=self.get_serializer()).data,
            'message': 'Пользователь успешно создан',
        })

    # def get_token(self, token):
    #     response = requests

    def get(self, request):
        token = request.query_params['code']
        response = requests.post(f'https://oauth.vk.com/access_token?client_id=51895987&client_secret=R7N5jmhZLiaKq8n44jgW&redirect_uri=http://localhost/api/auth/reg/redirect/&code={token}')
        token_acces = response.json()
        post = 1


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class VKLoginRedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        vk_login = VKLoginService()
        authorization_url, state = vk_login.get_authorization_url()
        request.session['vk_state'] = state
        return Response(authorization_url)
        # return redirect(authorization_url)


class VKLoginView(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')
        state = validated_data.get('state')

        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        if code is None or state is None:
            return Response({'error': 'Нет code или status'}, status=status.HTTP_400_BAD_REQUEST)

        session_state = request.session.get('vk_state')

        # if session_state is None:
        #     return Response({'error': 'state не вернулся'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # if state != session_state:
        #     return Response({'error': 'CSRF проверка не удалась'}, status=status.HTTP_400_BAD_REQUEST)

        vk_login = VKLoginService()
        vk_access_data = vk_login.get_access_data(code=code)

        user_info = vk_login.get_user_info(vk_access_data)

        user = vk_login.save_user(user_info)

        login(request, user)

        login_tokens = get_tokens_for_user(user)

        # return Response({'user_info': user_info,})
        return redirect('https://visualapp.ru/#/')
class UserConfirmEmailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response({'message': 'Почта подтверждена'})
        else:
            return Response({'message': 'Ошибка'})


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
        logger.info(f'User | {request.user}')
        serializer = AccountSerializer(instance=request.user)
        return Response({
            'user': serializer.data
        })

    def perform_destroy(self, instance):
        logger.info(f'User | {self.request.user}')
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
        logger.info(f'Payment | {request.user} {request.data}')
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


class CreatePaymentAcceptedView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        logger.info(f'Paymentrequest | {request.body}')
        response = json.loads(request.body)
        # response = request.data.get('payment_id')
        # user_id = request.data.get('user_id')
        # subscription = request.data.get('subscription')

        # payment = Payment.find_one(response['id'])
        user_id = response['object']['metadata']['user_id']
        subscription = response['object']['metadata']['subscription']
        if response['object']['status'] == 'succeeded':
            if subscription:
                user = Account.objects.get(id=user_id)
                user.subscription=subscription
                user.save()
                posts = Post.objects.filter(author_id=user_id)
                posts.update(premium=False)
                if subscription == 'premium':
                    posts = Post.objects.filter(author_id=user_id)
                    posts.update(premium=True)
                    return Response(200)

        else:
            return Response(400)


