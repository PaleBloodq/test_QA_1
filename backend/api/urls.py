from django.urls import path, include
from api import views

urlpatterns = [
    path('token/', include([
        path('refresh/', views.RefreshToken.as_view()),
        path('verify/', views.VerifyToken.as_view()),
        path('get/', views.GetToken.as_view()),
    ])),
    path('catalog/', include([
        path('search/', include([
            path('list/', views.SearchProducts.as_view()),
        ])),
        path('category/', views.GetCategories.as_view()),
        path('filters/', views.GetFilters.as_view()),
    ])),
    path('product/', include([
        path('<str:product_id>/', include([
            path('publications/', include([
                path('update/', views.UpdateProductPublications.as_view()),
            ])),
            path('', views.GetProduct.as_view()),
        ])),
    ])),
    path('publication/', include([
        path('<str:publication_id>/', include([
            path('', views.GetPublication.as_view()),
        ])),
    ])),
    path('order/', include([
        path('promocode/', include([
            path('check/', views.CheckPromoCode.as_view()),
        ])),
        path('buy/', views.CreateOrder.as_view()),
        path('chat/', views.ChatMessages.as_view()),
        path('update_status/', views.UpdateOrderStatus.as_view()),
    ])),
    path('profile/', include([
        path('update/', views.UpdateProfile.as_view()),
        path('orders/', views.Orders.as_view()),
        path('', views.Profile.as_view()),
    ])),
]
