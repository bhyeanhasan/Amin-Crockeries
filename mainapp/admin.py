from django.contrib import admin
from .models import Product
from .models import Card
from .models import Wishlist


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'res', 'tag']


admin.site.register(Card)

admin.site.register(Wishlist)
