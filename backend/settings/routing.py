from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/admin/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/order_manager/', consumers.OrderManagerConsumer.as_asgi()),
]
