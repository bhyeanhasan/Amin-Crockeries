from django.contrib import admin
from django.urls import path
from manage_order import views

urlpatterns = [
    path('order', views.order, name='order'),
    path('orderconfirm', views.orderConfirm, name='orderConfirm'),
    path('orderDetails/<id>', views.orderDetails, name='orderDetails'),
    path('wishlist', views.wishList, name='wishList'),
    path('addtowishlist/<id>', views.addToWishList, name='addToWishList'),
    path('deletewishitem/<id>', views.deleteWishItem, name='deleteWishItem'),
    path('cart', views.cart, name='cart'),
    path('addtocart/<id>', views.addToCart, name='addToCart'),
    path('deletecartitem/<id>', views.deleteCartItem, name='deleteCartItem'),

]
