from rest_framework import serializers
from .models import Follower
from notifications.models import Notification

class FollowerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        try:
            notification = Notification.objects.create(user=validated_data['author'])
            author = Follower.objects.create(
                author=validated_data['author'], follower=validated_data['follower'], notification_id=notification.id)
            return author
        except:
            return {'ошибка': 'Пользователь не найден'}

    def delete(self, validated_data):
        try:
            author = Follower.objects.get(
                author=validated_data['author'], follower=validated_data['follower'])
            author.delete()
            return author
        except:
            return {'ошибка': 'Пользователь не найден'}

    class Meta:
        model = Follower
        fields = ('author', 'follower')