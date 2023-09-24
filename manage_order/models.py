from datetime import datetime

from django.db import models
from manage_product.models import Product
from manage_user.models import Customer, Address


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "Product : " + self.product.name + " // Added by  " + self.customer.name


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "Product : " + self.product.name + " // Added by  " + self.customer.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    total_amount = models.FloatField(default=0.0)
    placed_at = models.DateTimeField(default=datetime.now())
    payment_status = models.CharField(max_length=50, default="Pending")
    status = models.CharField(max_length=500,default="Placed")

    def __str__(self):
        return "Amount : " + str(self.total_amount) + " // Placed at: " + str(self.placed_at.date())


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField()

    def __str__(self):
        return "Product : " + self.product.name + " // Orderded by: " + self.customer.name


class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.FloatField(default=5)
    comment = models.CharField(max_length=200, null=True, blank=True)
    review_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.product.name
