from django.contrib import admin
from .models import Product
from .models import Card
from .models import Wishlist

# Register your models here.
admin.site.register(Product)
admin.site.register(Card)
admin.site.register(Wishlist)
