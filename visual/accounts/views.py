import uuid
import json
from yookassa import Configuration, Payment
import logging
from visual import settings
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
from .services import VKLoginService, get_tokens_for_user, GoogleLoginService

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

logger = logging.getLogger('django')


class AccountViewSet(UserPostMixin, viewsets.ModelViewSet):
    """View для получения пользователей"""
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
    """"View для регистрации пользователей"""
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


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class VKLoginRedirectView(APIView):
    """View для перенаправления пользователей регистрирующихся через VK"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        vk_login = VKLoginService()
        authorization_url, state = vk_login.get_authorization_url()
        request.session['vk_state'] = state
        return Response(authorization_url)
        # return redirect(authorization_url)


class VKLoginView(PublicApi):
    """View для входа пользователей через VK"""

    class InputSerializer(serializers.Serializer):
        """Сериалайзер для проверки кода от VK"""
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


class GoogleLoginRedirectView(APIView):
    """View для перенаправления пользователей регистрирующихся через Google"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        google_login = GoogleLoginService()
        authorization_url, state = google_login.get_authorization_url()
        request.session['google_oauth2_state'] = state
        return Response(authorization_url)
        # return redirect(authorization_url)


class GoogleLoginView(PublicApi):
    """View для входа пользователей через Google"""

    class InputSerializer(serializers.Serializer):
        """Сериалайзер для проверки кода от Google"""
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

        google_login = GoogleLoginService()

        google_tokens = google_login.get_tokens(code=code)
        id_token_decoded = google_tokens.decode_id_token()
        user_info = google_login.get_user_info(google_tokens=google_tokens)

        # user_email = id_token_decoded["email"]
        # request_user_list = Account.objects.filter(email=user_email)
        # user = request_user_list.get() if request_user_list else None
        #
        # if user is None:
        #     return Response({"error": f"User with email {user_email} is not found."}, status=status.HTTP_404_NOT_FOUND)

        user = google_login.save_user(user_info)

        login(request, user)

        return Response({'user_info': user_info, })
        # return redirect('https://visualapp.ru/#/')


class UserConfirmEmailView(generics.RetrieveAPIView):
    """View для подтверждения почты пользователя"""
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
    """View профиля пользователя"""
    permission_classes = [IsUserProfile]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def retrive(self, request):
        """Данные пользователя"""
        logger.info(f'User | {request.user}')
        serializer = AccountSerializer(instance=request.user)
        return Response({
            'user': serializer.data
        })

    def perform_destroy(self, instance):
        """Удаление пользователя и переназначение его комментариев к пользователю deleted"""
        logger.info(f'User | {self.request.user}')
        deleted_user = Account.objects.get(username='deleted')
        user_id = instance.id
        all_user_comment = Comment.objects.filter(author_id=user_id)
        for comment in all_user_comment:
            comment.author_id = deleted_user.id
            comment.save()
        instance.delete()


class CreatePaymentView(generics.CreateAPIView):
    """View для оплаты подписки"""
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
    """View для проверки оплаты"""
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info(f'Paymentrequest | {request.body}')
        response = json.loads(request.body)
        user_id = response['object']['metadata']['user_id']
        subscription = response['object']['metadata']['subscription']
        if response['object']['status'] == 'succeeded':
            if subscription:
                user = Account.objects.get(id=user_id)
                user.subscription = subscription
                user.save()
                posts = Post.objects.filter(author_id=user_id)
                posts.update(premium=False)
                if subscription == 'premium':
                    posts = Post.objects.filter(author_id=user_id)
                    posts.update(premium=True)
                    return Response(200)
                return Response(200)

        else:
            return Response(400)
