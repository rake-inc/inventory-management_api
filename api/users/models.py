from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Roles(models.Model):
    user = models.ForeignKey(User)
    role = models.CharField(max_length=24)
