from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    res = models.IntegerField()
    tag = models.CharField(max_length=100)

    def get_absolute_url(self):
        return f"/details/{self.id}/"

    @property
    def addtocard(self):
        return f"/addtocard/{self.id}/"



class Card(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.IntegerField()

class Wishlist(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)