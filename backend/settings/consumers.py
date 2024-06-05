import logging
import json
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
        order_id = self.scope['url_route']['kwargs']['order_id']
        await self.channel_layer.group_add(order_id, self.channel_name)
        await self.channel_layer.group_add('new_order', self.channel_name)
        await self.accept()
