from django.urls import path
from custom_admin.consumers import NotificationConsumer, OrderManagerConsumer


websocket_urlpatterns = [
    path('ws/admin/notifications/', NotificationConsumer.as_asgi()),
    path('ws/order_manager/', OrderManagerConsumer.as_asgi()),
]
