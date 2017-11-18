from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Roles(models.Model):
<<<<<<< HEAD
    user = models.ForeignKey(User)
    department_manager = models.BooleanField(default=False)
    store_manager = models.BooleanField(default=True)
=======
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_manager = models.BooleanField(default=True)
    department_manager = models.BooleanField(default=False)
    approval = models.BooleanField(default=None)
>>>>>>> 1aa1e23fb1c5554a5d1e08537c70ac85c4df15b2
