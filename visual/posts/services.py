from accounts.models import Account
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from accounts.serializers import AccountSerializer
from .models import Like


def add_like(obj, user):
    """Лайк"""
    obj_type = ContentType.objects.get_for_model(obj)
    author = obj.author
    notification = Notification.objects.create(user=author)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user, notification_id=notification.id)
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

