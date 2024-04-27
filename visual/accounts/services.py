import random
import string
import requests
import jwt
from posts.models import Post
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from urllib.parse import urlencode
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from .serializers import RegisterSerializer

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Получение токенов для пользователя"""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def my_post(user):
    return Post.objects.filter(author_id=user.id)


def random_string(length):
    """Создание случайной строки"""
    string = get_random_string(length=length, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789')
    return string


@define
class VKLoginCredentials:
    client_id: str
    service_key: str
    client_secret: str


class VKLoginService:
    """Класс для обработки данных от VK"""
    API_URI = reverse_lazy("api:callback")

    VK_AUTH_URL = 'https://oauth.vk.com/authorize'
    VK_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth.vk.com/access_token'
    VK_USER_INFO_URL = 'https://api.vk.com/method/users.get'
    VK_API_VERSION = '5.199'

    def __init__(self):
        self.credentials = vk_login_get_credentials()

    @staticmethod
    def generate_state_session_token(length=30):
        letters = string.ascii_letters
        state = ''.join(random.choice(letters) for i in range(length))
        return state

    def get_redirect_uri(self):
        """Делаем URI для перенаправления пользователя"""
        # domain = Site.objects.get_current().domain
        domain = 'http://localhost:80'
        api_uri = self.API_URI
        redirect_uri = f'{domain}{api_uri}'
        return redirect_uri

    def get_authorization_url(self):
        """Создаем URL для перенаправления пользователя на стринцу входа VK"""
        redirect_uri = self.get_redirect_uri()
        state = self.generate_state_session_token()
        params = {
            'client_id': self.credentials.client_id,
            'redirect_uri': redirect_uri,
            'display': 'page',
            'scope': '12',
            'response_type': 'code',
            'state': state,
            'v': self.VK_API_VERSION,
        }
        query_params = urlencode(params)
        authorization_url = f'{self.VK_AUTH_URL}?{query_params}'
        return authorization_url, state

    def get_access_data(self, code):
        """Получение данных от VK"""
        redirect_uri = self.get_redirect_uri()

        data = {
            'client_id': self.credentials.client_id,
            'code': code,
            'client_secret': self.credentials.client_secret,
            'redirect_uri': redirect_uri,
        }

        response = requests.post(self.VK_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            return Response({'error': 'Failed to obtain access token from Google.'})

        vk_access_data = response.json()

        return vk_access_data

    def get_user_info(self, vk_access_data):
        """Получение информации о юзере"""
        data = {
            'user_ids': vk_access_data['user_id'],
            'access_token': vk_access_data['access_token'],
            'fields': 'photo_max_orig',
            'v': self.VK_API_VERSION,
        }
        response = requests.post(self.VK_USER_INFO_URL, data=data)

        user_info = response.json()

        return user_info

    def save_user(self, user_info):
        """Сохранение юзера в базе"""
        password = random_string(10)
        random_email = f'{random_string(6)}_vk@example.com'  # ПРОВЕРЯТЬ ПОЧТУ НА УНИКАЛЬНОСТЬ
        username = f"vk_{user_info['response'][0]['id']}"
        data = {
            'username': username,
            'email': random_email,
            'password': password,
            'password2': password
        }
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.first_name = user_info['response'][0]['first_name']
        user.last_name = user_info['response'][0]['last_name']
        user.save()
        return user


def vk_login_get_credentials() -> VKLoginCredentials:
    """Получение данных для входа"""
    client_id = settings.SOCIAL_AUTH_VK_CLIENT_ID
    service_key = settings.SOCIAL_AUTH_VK_SERVICE_ACCESS_KEY
    client_secret = settings.SOCIAL_AUTH_VK_SECRET_KEY

    if not client_id:
        raise ImproperlyConfigured('SOCIAL_AUTH_VK_CLIENT_ID отсутствует')

    if not service_key:
        raise ImproperlyConfigured('SOCIAL_AUTH_VK_PROTECTED_KEY отсутствует')

    if not client_secret:
        raise ImproperlyConfigured('SOCIAL_AUTH_VK_SECRET_KEY отсутствует')

    credentials = VKLoginCredentials(
        client_id=client_id,
        service_key=service_key,
        client_secret=client_secret
    )

    return credentials


@define
class GoogleLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@define
class GoogleAccessTokens:
    id_token: str
    access_token: str

    def decode_id_token(self):
        """Расшифрование токена"""
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={'verify_signature': False})
        return decoded_token


class GoogleLoginService:
    """Класс для обработки данных от Google"""
    API_URI = reverse_lazy('api:callback_google')
    GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self.credentials = google_login_get_credentials()

    @staticmethod
    def generate_state_session_token(length=30):
        letters = string.ascii_letters
        state = ''.join(random.choice(letters) for i in range(length))
        return state

    def get_redirect_uri(self):
        """Делаем URI для перенаправления пользователя"""
        # domain = Site.objects.get_current().domain
        domain = 'http://localhost:8000'
        api_uri = self.API_URI
        redirect_uri = f'{domain}{api_uri}'
        return redirect_uri

    def get_authorization_url(self):
        """Создаем URL для перенаправления пользователя на стринцу входа Google"""
        redirect_uri = self.get_redirect_uri()

        state = self.generate_state_session_token()

        params = {
            'response_type': 'code',
            'client_id': self.credentials.client_id,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(self.SCOPES),
            'state': state,
            'access_type': 'offline',
            'include_granted_scopes': 'true',
            'promt': 'select_account',
        }

        query_params = urlencode(params)
        authorization_url = f'{self.GOOGLE_AUTH_URL}?{query_params}'

        return authorization_url, state

    def get_tokens(self, code):
        """Получение токенов"""
        redirect_uri = self.get_redirect_uri()

        data = {
            'code': code,
            'client_id': self.credentials.client_id,
            'client_secret': self.credentials.client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            return Response({'error': 'Failed to obtain access token from Google.'})

        tokens = response.json()

        google_tokens = GoogleAccessTokens(
            id_token=tokens['id_token'],
            access_token=tokens['access_token']
        )

        return google_tokens

    def get_user_info(self, *, google_tokens):
        """Получение информации о юзере"""
        access_token = google_tokens.access_token

        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={'access_token': access_token}
        )

        if not response.ok:
            return Response({'error': 'Failed to obtain user info from Google.'})

        return response.json()

    def save_user(self, user_info):
        """Сохранение юзера в базе"""
        password = random_string(10)
        username = f"google_{user_info['sub']}"
        data = {
            'username': username,
            'email': user_info['email'],
            'password': password,
            'password2': password
        }
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.first_name = user_info['given_name']
        user.last_name = user_info['family_name']
        user.save()
        return user


def google_login_get_credentials() -> GoogleLoginCredentials:
    """Получение данных для входа"""
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = settings.SOCIAL_AUTH_GOOGLE_CLIENT_SECRET
    project_id = settings.SOCIAL_AUTH_GOOGLE_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("SOCIAL_AUTH_GOOGLE_CLIENT_ID отсутствует")

    if not client_secret:
        raise ImproperlyConfigured("SOCIAL_AUTH_GOOGLE_CLIENT_SECRET отсутствует")

    if not project_id:
        raise ImproperlyConfigured("SOCIAL_AUTH_GOOGLE_PROJECT_ID отсутствует")

    credentials = GoogleLoginCredentials(
        client_id=client_id,
        client_secret=client_secret,
        project_id=project_id
    )

    return credentials
