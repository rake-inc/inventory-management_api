from .models import Roles, RoleApproval
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ('user', 'store_manager', 'department_manager')

class ApproveRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleApproval
        fields = ('user','approval')