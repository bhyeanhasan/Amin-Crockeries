from django.contrib import admin
from django.urls import path, include
from manage_api import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('product-list', views.product_list, name='manage_api'),
    path('custom/<int:pk>/', views.product_details, name='custom'),
    path('users', views.UserViewSet.as_view({"get": "list"}), name='users'),
    path('user-details/<int:pk>', views.UserViewSet.as_view({"get": "retrieve"}), name='users'),
    path('products', views.ProductViewSet.as_view({"get": "list"}), name='products'),
    path('product-details/<int:pk>', views.ProductViewSet.as_view({"get": "retrieve"}), name='product-details'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
