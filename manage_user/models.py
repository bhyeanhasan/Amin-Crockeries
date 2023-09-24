from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    registered_at = models.DateTimeField(default=datetime.now())
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)

    def __str__(self):
        return self.name



class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    alternate_mobile = models.CharField(max_length=50, blank=True, null=True)
    division = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    upazila = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.customer.name)

    def get_absolute_url(self):
        return f"{self.id}"
