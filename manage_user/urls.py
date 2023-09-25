from django.contrib import admin
from django.urls import path
from manage_user import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgetpassword', views.forgetPassword, name='forgetPassword'),
    path('profile', views.profile, name='profile'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('updatepass', views.updatepass, name='updatepass'),
    path('address', views.addressBook, name='address'),
    path('addAddress', views.addAddress, name='addAddress'),
    path('address/<id>/', views.showAddress, name='showAddress'),
    path('deleteddress/<id>/', views.deleteAddress, name='deleteAddress'),
    path('editaddress', views.editAddress, name='editAddress'),
]


