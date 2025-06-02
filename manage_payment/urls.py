from django.contrib import admin
from django.urls import path
from manage_payment import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('<orderId>', views.pay, name='payment'),
    path('payment_check/<id>', views.payment_check, name='payment_check'),

    # Stripe URLs
    path('stripe/config/', views.get_stripe_publishable_key, name='stripe_config'),
    path('stripe/checkout-session/<int:order_id>/', views.checkout_session_stripe, name='checkout_session_stripe'),
    path('stripe/success/<int:order_id>/', views.payment_success_stripe, name='payment_success_stripe'),
    path('stripe/cancel/<int:order_id>/', views.payment_cancel_stripe, name='payment_cancel_stripe'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
