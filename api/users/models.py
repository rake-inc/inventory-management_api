from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    store_manager = models.BooleanField(default=True)
    department_manager = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class RoleApproval(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
