from django.contrib import admin
from .models import Customer, Address


# admin.site.register(Customer)
# admin.site.register(Address)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'address_name']
