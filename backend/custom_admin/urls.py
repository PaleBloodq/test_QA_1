from django.urls import path
from custom_admin import views

urlpatterns = [
    path('admin/chat/<str:order_id>/', views.Chat.as_view()),
    path('admin/chat/', views.Chat.as_view()),
]
