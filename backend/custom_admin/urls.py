from django.urls import path
from . import views


urlpatterns = [
    path('admin/order_manager/', views.OrderManager.as_view(), name='order_manager'),
]
