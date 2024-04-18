from django.urls import path, include
from api import views

urlpatterns = [
    path('catalog/category/', views.GetCategories.as_view()),
]
