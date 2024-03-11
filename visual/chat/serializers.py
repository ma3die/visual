from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import AccountSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = AccountSerializer()
    receiver = AccountSerializer()
    last_message = serializers.SerializerMethodField()
    # last_message = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields =  ('initiator', 'receiver', 'last_message')

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message).data


class ConversationSerializer(serializers.ModelSerializer):
    initiator = AccountSerializer()
    receiver = AccountSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'
            # ('initiator', 'receiver', 'message_set')
