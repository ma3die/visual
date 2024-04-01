import random
import string
from django.db import transaction
from accounts.models import Account
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from accounts.serializers import AccountSerializer
from .models import Like, Post

@transaction.atomic
def add_like(obj, user):
    """Лайк"""
    obj_type = ContentType.objects.get_for_model(obj)
    author = obj.author

    if obj.author_id != user.id:
        notification = Notification.objects.create(user=author)
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=user, notification_id=notification.id)
    else:
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    """Удалить лайк"""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user).delete()


def is_like(obj, user):
    """Проверяем лайкнул ли user obj"""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_likes(obj):
    """Получаем всех пользователей, которые лайкнули obj"""
    obj_type = ContentType.objects.get_for_model(obj)
    users = Account.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)
    return AccountSerializer(instance=users, many=True).data


def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_user(user):
    '''Функция для заполнения данных для анонимного пользователя'''
    if user.is_anonymous:
        random_username = f"{randomString(10)}_guest"
        random_email = f"{randomString(5)}_guest@example.com"
        guest_user = Account.objects.create(username=random_username, is_active=False, email=random_email)
        return guest_user
    else:
        pass