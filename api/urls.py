from django.urls import path, include
from api import views

urlpatterns = [
    path('', views.test_view)
]
