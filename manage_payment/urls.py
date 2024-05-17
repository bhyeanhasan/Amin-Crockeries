from django.contrib import admin
from django.urls import path
from manage_payment import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('<orderId>', views.pay, name='payment'),
    path('payment_check/<id>', views.payment_check, name='payment_check'),
]
