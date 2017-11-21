import logging
from utils import mapper
from postgres import fields
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
        """
        Private access specifier to add user id for the creation of role entity model
        :param user_id:
        :param role_dict:
        :return:
        """
        role_dict[fields.USER] = user_id
        return role_dict

    def post(self, request):
        """
        POST method for the creation of auth_user and users_role model
        :param request:
        :return:
        """
        try:
            user_dict, role_dict = mapper.re_map_user_roles(request.data)
            user_serializer = UserSerializer(data=user_dict)
            if user_serializer.is_valid():
                user_serializer.save()
            user_id = User.objects.only(fields.USER_PK).get(username=request.data.get(fields.USERNAME)).id
            processed_role_data = self._add_user_id(user_id, role_dict)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                user_obj = User.objects.get(pk=user_id)
                RoleApproval.objects.create(user=user_obj)
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
        return Response(status=HTTP_417_EXPECTATION_FAILED)


class RoleDetails(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        """
        GET method for querying the users_roles model based on url query
        :param request:
        :return:
        """
        try:
            param_dict = mapper.re_map_role_params(request.query_params)
            query = User.objects.only(fields.USER_PK).get(**param_dict).id
            username = User.objects.only(fields.USERNAME).get(id=query).username
            data_obj = Role.objects.filter(user_id=query)
            role_serializer = RoleSerializer(data_obj, many=True)
            response_data = mapper.re_map_role_response(role_serializer.data, username)
            return Response(response_data, status=HTTP_200_OK)
        except Exception as e:
            logging.error("Exception Reached %s " % e)
            message = {
                "message": "User not found"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)
