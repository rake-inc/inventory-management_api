from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Roles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_manager = models.BooleanField(default=True)
    department_manager = models.BooleanField(default=False)

class RoleApproval(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	approval = models.BooleanField(default=False)
