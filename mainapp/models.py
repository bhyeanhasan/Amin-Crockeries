from django.db import models


# Create your models here.
class DP(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    res = models.IntegerField()
    tag = models.CharField(max_length=100)

    def get_absolute_url(self):
        return f"/details/{self.id}/"


