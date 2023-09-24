from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name




# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    unit_price = models.FloatField(default=0.0)
    stock_quantity = models.IntegerField(default=20)
    img = models.ImageField(upload_to='pics', blank=True, null=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/details/{self.id}/"

    @property
    def addtocard(self):
        return f"/addtocard/{self.id}/"

    @property
    def deletefromcart(self):
        return f"/deletefromcart/{self.id}/"

    @property
    def deleteallcart(self):
        return f"/deleteallcart/{self.id}/"

    @property
    def addtowish(self):
        return f"/addtowish/{self.id}/"
