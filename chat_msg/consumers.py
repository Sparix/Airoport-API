import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from chat_msg.models import ChatSupport, ChatMessage
from chat_msg.serializers import ChatMessageSerializerBase


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope.get('user_id', "")

        self.user = await self.get_user(self.user_id)

        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']

        self.chatroom = await self.get_chatroom(self.chatroom_id)

        if not await self.is_user_in_chatroom(self.user, self.chatroom):
            await self.close()
            return

        await self.channel_layer.group_add(
            str(self.chatroom_id), self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            str(self.chatroom_id), self.channel_name
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = await self.create_message(body)

        event = {
            "type": "chat.message",
            "message_id": message.id,
        }
        await self.channel_layer.group_send(
            str(self.chatroom_id), event
        )

    @database_sync_to_async
    def create_message(self, body):
        return ChatMessage.objects.create(
            body_msg=body,
            user=self.user,
            support_msg=self.chatroom,
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.get(id=user_id)

    @database_sync_to_async
    def get_chatroom(self, chatroom_id):
        return get_object_or_404(ChatSupport, id=chatroom_id)

    @database_sync_to_async
    def get_message_data(self, message):
        return ChatMessageSerializerBase(message).data

    @database_sync_to_async
    def is_user_in_chatroom(self, user, chatroom):
        return user in chatroom.user_list.all()

    async def chat_message(self, event):
        message = await self.get_message(event['message_id'])
        message_data = await self.get_message_data(message)
        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def get_message(self, message_id):
        return ChatMessage.objects.get(id=message_id)
