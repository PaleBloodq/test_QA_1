import logging
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        await self.channel_layer.group_send("admin_notifications", {"type": "admin_message", "message": message})

    async def admin_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))


class OrderManagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('order_manager', self.channel_name)
        await self.accept()
        await self.send(text_data='SOME DATA')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('order_manager', self.channel_name)

    async def receive(self, text_data):
        from api import models
        data = json.loads(text_data)
        match data.get('type'):
            case 'new_message':
                await sync_to_async(models.ChatMessage.objects.create)(
                    order_id=data.get('order_id'),
                    text=data.get('text'),
                    manager=data.get('manager')
                )
    
    async def chat_message(self, event: dict):
        await self.send(text_data=json.dumps(event))
    
    async def new_order(self, event: dict):
        await self.send(text_data=json.dumps(event))
