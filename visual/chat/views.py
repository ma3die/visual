from django.shortcuts import render, redirect, reverse
from .models import Conversation
from rest_framework.decorators import api_view, permission_classes #
from rest_framework import permissions
from rest_framework.response import Response
from accounts.models import Account
from .serializers import ConversationListSerializer, ConversationSerializer
from django.db.models import Q



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def start_convo(request, ):
    data = request.data
    username = data.pop('username')
    try:
        participant = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return Response({'message': 'Получатель не найден'})

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        serializer = ConversationSerializer(instance=conversation)
        return Response(serializer.data)
            # Response(ConversationSerializer(instance=conversation).data))


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Чат не найден'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    data = serializer.data
    return Response(data)