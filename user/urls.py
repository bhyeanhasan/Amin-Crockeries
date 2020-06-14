from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('profile', views.profile, name = 'profile'),
    path('product', views.product, name = 'product'),
    path('updateprofile', views.updateprofile, name = 'updateprofile'),
    path('updateUser', views.updateUser, name = 'updateUser'),
    path('updatepass', views.updatepass, name = 'updatepass'),
]
