import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatGroup, AdvUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def new_message(self, message, chatslug, user):
        Message.objects.create(text=message, group=ChatGroup.objects.get(slug=chatslug), sender=AdvUser.objects.get(pk=user))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chatslug = text_data_json['chatslug']
        user = text_data_json['user']
        await self.new_message(message=message, chatslug=chatslug, user=user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': self.scope['user'].username.title(),
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }, ensure_ascii=False))
