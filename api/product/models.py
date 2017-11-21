from django.db import models


# Create your models here.

class ProductDetails(models.Model):
    name = models.CharField(max_length=64)
    vendor = models.CharField(max_length=64)
    batch_num = models.IntegerField()
    price = models.IntegerField()
    batch_date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    status = models.CharField(max_length=16)

    def __str__(self):
        return self.pk + " " + self.name
