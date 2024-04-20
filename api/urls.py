from django.urls import path, include
from api import views

urlpatterns = [
    path("product/<str:product_id>/", views.GetProduct.as_view()),
    path("publication/<str:publication_id>/", views.GetPublication.as_view()),
    path('catalog/category/', views.GetCategories.as_view()),
    path('catalog/filters/', views.GetFilters.as_view()),
    path('catalog/search/list/', views.SearchProducts.as_view()),
]
