from django.contrib import admin
from django.urls import path,include
from manage_api import views

urlpatterns = [
    path('', views.product_list, name='manage_api'),
    path('custom/<int:pk>/', views.product_details, name='custom'),
]