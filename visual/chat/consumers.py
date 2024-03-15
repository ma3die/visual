import base64
import json
import secrets
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from accounts.models import Account
from .models import Message, Conversation
from .serializers import MessageSerializer
from accounts.models import Account


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # def get_receiver(self):
    #     username = self.room_name.split("__")
    #     return username
    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        # user = self.get_receiver()
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        receiver_id = text_data_json['receiver']
        message_type = text_data_json['type']
        sender = self.scope['user']
        sender_id = sender.id
        receiver = Account.objects.get(id=receiver_id)
        conversation = Conversation.objects.get(id=int(self.room_name))

        if message_type == 'read_message':
            messages_to_me = Message.objects.filter(conversation_id_id=conversation.id, receiver=sender, read=False)
            messages_to_me.update(read=True)

            # Update the unread message count
            unread_count = Message.objects.filter(receiver=sender, read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                sender.username + '__notifications',
                {
                    'type': 'unread_count',
                    'unread_count': unread_count
                }
            )

        # Send message to room group
        if message_type == 'chat_message':
            attachment = text_data_json.get("attachment")
            if attachment:
                file_str, file_ext = attachment["data"], attachment["format"]

                file_data = ContentFile(
                    base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
                )
                _message = Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    attachment=file_data,
                    text=text_data_json['message'],
                    conversation_id=conversation,
                )
            else:
                _message = Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    text=text_data_json['message'],
                    conversation_id=conversation,
                )
        # chat_type = {"type": "chat_message"}
        # return_dict = {"sender_id": sender_id, **chat_type, **text_data_json}
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,{
                    'type': 'chat_message',
                    'message': MessageSerializer(_message).data
                }
            )

            notification_group_name = receiver.username + '__notifications'
            async_to_sync(self.channel_layer.group_send)(
                notification_group_name, {
                    "type": "new_message_notification",
                    "name": sender.username,
                    "message": MessageSerializer(_message).data,
                }
            )




    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        text_data = json.dumps(text_data_json['message'])
        # message, sender_id, attachment = (
        #     text_data_json["message"],
        #     text_data_json["sender_id"],
        #     text_data_json.get("attachment"),
        # )

        # conversation = Conversation.objects.get(id=int(self.room_name))
        # sender = Account.objects.get(id=sender_id)
        # receiver = self.scope['user']

        # Attachment
        # if attachment:
        #     file_str, file_ext = attachment["data"], attachment["format"]
        #
        #     file_data = ContentFile(
        #         base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
        #     )
        #     _message = Message.objects.create(
        #         sender=sender,
        #         receiver=receiver,
        #         attachment=file_data,
        #         text=message,
        #         conversation_id=conversation,
        #     )
        # else:
        #     _message = Message.objects.create(
        #         sender=sender,
        #         receiver=receiver,
        #         text=message,
        #         conversation_id=conversation,
        #     )
        # serializer = MessageSerializer(instance=_message)
        # Send message to WebSocket
        # data = serializer.data
        # data['user'] = user
        # text_data = json.dumps(
        #     data)
        self.send(text_data)

    def new_message_notification(self, event):
        text_data = json.dumps(event)
        self.send(text_data)

    def unread_count(self, event):
        text_data = json.dumps(event)
        self.send(text_data)
    # def send_notification(self, message):
    #     self.send(text_data=json.dumps({
    #         "type": "notifification",
    #         "message": message
    #     }))


class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None

    def connect(self):
        self.user = self.scope['user']
        self.accept()

        # private notification group
        self.notification_group_name = self.user.username + '__notifications'
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # Send count of unread messages
        unread_count = Message.objects.filter(receiver=self.user, read=False).count()
        data = {
            'type': 'unread_type',
            'unread_count': unread_count
        }
        text_data = json.dumps(data)
        self.send(text_data)


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )

    def new_message_notification(self, event):
        text_data = json.dumps(event)
        self.send(text_data)

    def unread_count(self, event):
        text_data = json.dumps(event)
        self.send(text_data)