from django.db import models


# Create your models here.

class ProductDetails(models.Model):
    product_id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=64)
    vendor = models.CharField(max_length=64)
    batch_num = models.IntegerField()
    batch_date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    status = models.CharField(max_length=16)
