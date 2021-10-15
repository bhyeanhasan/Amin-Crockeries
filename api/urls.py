from django.contrib import admin
from django.urls import path,include
from api import views

urlpatterns = [
    path('', views.product_list, name='api'),
    path('custom/<int:pk>/', views.product_details, name='custom'),
]