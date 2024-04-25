from django.urls import path
from api import views

urlpatterns = [
    path('product/<str:product_id>/publications/update/', views.UpdateProductPublications.as_view()),
    path('product/<str:product_id>/', views.GetProduct.as_view()),
    path('publication/<str:publication_id>/', views.GetPublication.as_view()),
    path('catalog/category/', views.GetCategories.as_view()),
    path('catalog/filters/', views.GetFilters.as_view()),
    path('catalog/search/list/', views.SearchProducts.as_view()),
    path('order/buy/', views.CreateOrder.as_view()),
    path('order/promocode/check/', views.CheckPromoCode.as_view()),
    path('profile/update/', views.UpdateProfile.as_view()),
    path('profile/orders/', views.Orders.as_view()),
    path('profile/', views.Profile.as_view()),
    path('token/refresh/', views.RefreshToken.as_view()),
    path('token/verify/', views.VerifyToken.as_view()),
    path('token/get/', views.GetToken.as_view()),
]
