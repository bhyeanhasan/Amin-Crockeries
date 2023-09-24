from django.contrib import admin
from .models import Cart, Wishlist, OrderedItem, Order, Review


# admin.site.register(Cart)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity']


# admin.site.register(Wishlist)
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer']


# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'placed_at', 'status']


# admin.site.register(OrderedItem)
@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity', 'unit_price', 'order']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product','customer', 'rating', 'comment', 'review_time']