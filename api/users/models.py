from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Roles(models.Model):
    user = models.ForeignKey(User)
    store_manager = models.BooleanField(default=True)
    department_manager = models.BooleanField(default=False)
