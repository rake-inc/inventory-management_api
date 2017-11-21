import logging
from utils import mapper
from .models import Role, RoleApproval
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializer import UserSerializer, RoleSerializer, ApproveRoleSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_400_BAD_REQUEST


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        r_data = {}
        try:
            r_data.update(store_manager=request.data.pop("store_manager"))
            r_data.update(department_manager=request.data.pop("department_manager"))
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
            _id = User.objects.only('id').get(username=request.data.get("username")).id
            r_data.update(user_id=_id)
            processed_role_data = mapper.re_map_user_roles(r_data)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                user_obj = User.objects.get(pk=_id)
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
            return Response(role_serializer.data, status=HTTP_200_OK)
        except Exception as e:
            logging.error("Exception Reached %s " % e)
            message = {
                "message": "User not found"
            }
            return Response(message, status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializers = ApproveRoleSerializer(data=request.data)
        try:
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=HTTP_201_CREATED)
            else:
                return Response(serializers.data, status=HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
            return Response(serializers.errors, status=HTTP_417_EXPECTATION_FAILED)
