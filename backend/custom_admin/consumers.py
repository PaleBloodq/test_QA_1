import logging
import base64
import uuid
import json
from PIL import Image
from io import BytesIO
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
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
    
    async def receive(self, text_data):
        from django.contrib.auth.models import User
        from api import models, senders
        data = json.loads(text_data)
        match data.get('type'):
            case 'new_message':
                message = await models.ChatMessage.objects.acreate(
                    order_id=data.get('order_id'),
                    text=data.get('text'),
                    manager=await User.objects.aget(id=data.get('manager')),
                )
                for image in data.get('images', []):
                    await sync_to_async(self.save_image)(image, message)
                await sync_to_async(senders.send_chat_message)(message)
            case 'accept_order':
                order = await models.Order.objects.aget(id=data.get('order_id'))
                order.status = models.Order.StatusChoices.IN_PROGRESS
                order.manager = self.scope['user']
                await order.asave()
                await senders._send_order_manager(
                    'accept_order',
                    order_id=str(order.id),
                    manager_id=self.scope['user'].id
                )
            case 'order_completed':
                order = await models.Order.objects.aget(id=data.get('order_id'))
                order.status = models.Order.StatusChoices.COMPLETED
                await order.asave()
                await senders._send_order_manager(
                    'order_completed',
                    order_id=str(order.id),
                    manager_id=self.scope['user'].id
                )
            case 'my_orders_tab':
                await self.send(text_data=json.dumps({
                    'type': 'my_orders',
                    'orders': await sync_to_async(self.get_orders)(
                        limit=data.get('limit', 20),
                        offset=data.get('offset', 0),
                        query=dict(
                            status=models.Order.StatusChoices.IN_PROGRESS,
                            manager=self.scope['user'].pk,
                        )
                    ),
                }))
            case 'all_orders_tab':
                await self.send(text_data=json.dumps({
                    'type': 'all_orders',
                    'orders': await sync_to_async(self.get_orders)(
                        limit=data.get('limit', 20),
                        offset=data.get('offset', 0),
                        query=dict(
                            status=models.Order.StatusChoices.PAID,
                            manager=None,
                        )
                    ),
                }))
            case 'completed_orders_tab':
                await self.send(text_data=json.dumps({
                    'type': 'completed_orders',
                    'orders': await sync_to_async(self.get_orders)(
                        limit=data.get('limit', 20),
                        offset=data.get('offset', 0),
                        query=dict(
                            status=models.Order.StatusChoices.COMPLETED,
                        )
                    ),
                }))
            case 'get_order':
                await self.send(text_data=json.dumps({
                    'type': 'get_order',
                    'order': await sync_to_async(self.get_order_by_id)(
                        order_id=data.get('order_id')
                    ),
                }))
    
    async def chat_message(self, event: dict):
        await self.send(text_data=json.dumps(event))
    
    async def new_order(self, event: dict):
        await self.send(text_data=json.dumps(event))
    
    async def accept_order(self, event: dict):
        await self.send(text_data=json.dumps(event))
    
    async def order_completed(self, event: dict):
        await self.send(text_data=json.dumps(event))
    
    def get_orders(self, limit: int, offset: int, query: dict = {}):
        from api import models
        from api.serializers.order_manager import OrderPreviewSerializer
        return OrderPreviewSerializer(models.Order.objects.filter(**query)[offset:limit], many=True).data
    
    def get_order_by_id(self, order_id: str) -> dict:
        from api import models
        from api.serializers.order_manager import OrderSerializer
        return OrderSerializer(
            models.Order.objects.get(id=order_id)
        ).data
    
    def save_image(self, image: str, message):
        from api import models
        order_message_image = models.OrderMessageImage.objects.create(chat_message=message)
        img = Image.open(BytesIO(base64.b64decode(image)))
        img_io = BytesIO()
        img.save(img_io, format="WEBP", quality=50)
        img_io.seek(0)
        order_message_image.image.save(f'photo_{uuid.uuid4().hex}.webp', ContentFile(img_io.getvalue()), save=True)
        return order_message_image
