from .models import Role
from postgres import fields
from rest_framework import serializers
from django.contrib.auth.models import User

USER_SERIALIZER_FIELDS = (
    fields.USERNAME,
    fields.FIRST_NAME,
    fields.LAST_NAME,
    fields.USER_PASSWORD,
    fields.USER_EMAIL,
)

ROLE_SERIALIZER_FIELDS = (
    fields.USER,
    fields.IS_STORE_MANAGER,
    fields.IS_DEPARTMENT_MANAGER
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = USER_SERIALIZER_FIELDS

    def create(self, validated_data):
        """
        Creates auth_user object with password validation
        :param validated_data:
        :return:
        """
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data[fields.USER_PASSWORD])
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ROLE_SERIALIZER_FIELDS
