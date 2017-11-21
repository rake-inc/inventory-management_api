from django.contrib import admin
from .models import Role, RoleApproval

# Register your models here.
admin.site.register(Role)
admin.site.register(RoleApproval)
