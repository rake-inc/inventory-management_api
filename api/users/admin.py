from django.contrib import admin
from django.contrib.auth.models import User
from .models import Role, RoleApproval
from postgres import fields

# Register your models here.
ROLE_ADMIN_FIELDS = [
    fields.USER,
    fields.IS_STORE_MANAGER,
    fields.IS_DEPARTMENT_MANAGER
]
ROLE_APPROVAL_ADMIN_FIELDS = [
    fields.USER,
    fields.IS_APPROVED,
]


class RoleAdmin(admin.ModelAdmin):
    list_display = ROLE_ADMIN_FIELDS


class RoleApprovalAdmin(admin.ModelAdmin):
    list_display = ROLE_APPROVAL_ADMIN_FIELDS


admin.site.register(Role, RoleAdmin)
admin.site.register(RoleApproval, RoleApprovalAdmin)
