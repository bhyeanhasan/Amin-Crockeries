from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    category = (
        ('pitol', 'Pitol'),
        ('dinner', 'Dinner Set'),
        ('plastic', 'Plastic'),
        ('cooker','Cooker'),
    )
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    res = models.IntegerField()
    tag = models.CharField(max_length=100, choices=category)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/details/{self.id}/"

    @property
    def addtocard(self):
        return f"/addtocard/{self.id}/"

    @property
    def addtowish(self):
        return f"/addtowish/{self.id}/"


class Card(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.IntegerField()

    def __str__(self):
        return self.product.name+" is added by > "+self.customer.username

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name+" is added by > "+self.customer.username
