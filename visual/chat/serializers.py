from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import AccountSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Сериайлазер сообщений"""

    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода всех чатов"""
    initiator = AccountSerializer()
    receiver = AccountSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('initiator', 'receiver', 'last_message')

    def get_last_message(self, instance):
        """Отображение последнего сообщения в списке чатов"""
        message = instance.message_set.first()
        return MessageSerializer(instance=message).data


class ConversationSerializer(serializers.ModelSerializer):
    """Сериалайзер чата"""
    initiator = AccountSerializer()
    receiver = AccountSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'
        # ('initiator', 'receiver', 'message_set')
