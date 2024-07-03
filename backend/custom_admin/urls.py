from django.urls import path
from . import views
from settings import FORCE_SCRIPT_NAME


urlpatterns = [
    path('admin/order_manager/', views.OrderManager.as_view(), {'FORCE_SCRIPT_NAME': FORCE_SCRIPT_NAME}, 'order_manager'),
]
