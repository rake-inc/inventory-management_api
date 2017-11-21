import logging
from utils import mapper
from .models import Role, RoleApproval
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer, RoleSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_400_BAD_REQUEST


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def _add_user_id(self, user_id, role_dict):
        role_dict["user"] = user_id
        return role_dict

    def post(self, request):
        try:
            user_dict, role_dict = mapper.re_map_user_roles(request.data)
            user_serializer = UserSerializer(data=user_dict)
            if user_serializer.is_valid():
                user_serializer.save()
            user_id = User.objects.only('id').get(username=request.data.get("username")).id
            processed_role_data = self._add_user_id(user_id, role_dict)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                user_obj = User.objects.get(pk=user_id)
                RoleApproval.objects.create(user=user_obj, approval=False)
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
        return Response(status=HTTP_417_EXPECTATION_FAILED)


class RoleDetails(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        try:
            param_dict = mapper.re_map_role_params(request.query_params)
            query = User.objects.only('id').get(**param_dict).id
            data_obj = Role.objects.filter(user_id=query)
            role_serializer = RoleSerializer(data_obj, many=True)
            print role_serializer.data
            return Response(role_serializer.data, status=HTTP_200_OK)
        except Exception as e:
            logging.error("Exception Reached %s " % e)
            message = {
                "message": "User not found"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)
