import logging
from ast import literal_eval
from .models import Roles, RoleApproval
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializer import UserSerializer, RoleSerializer, ApproveRoleSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_400_BAD_REQUEST

# Create your views here.

class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def _re_map_roles(self, serializers_dict):
        result = {}
        for key in serilizers_dict.keys():
            result[key] = serializers_dict.get(key)
        result['user'] = serializer.get('user_id')
        return result

    def post(self, request):
        r_data = {}
        try:
            user_serializer = UserSerializer(data=request.data)
            r_data.update(store_manager=request.data.pop("store_manager"))
            r_data.update(department_manager=request.data.pop("department_manager"))
            if user_serializer.is_valid():
                user_serializer.save()
            _id = User.objects.only('id').get(username=request.data.get("username")).id
            logging.info("User created with ID %s" %_id)
            r_data.update(user_id=_id)
            processed_role_data = self._re_map_roles(r_data)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                RoleApproval.objects.create(user=_id,approval=False)
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
        return Response(status=HTTP_417_EXPECTATION_FAILED)


class RoleDetails(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [JSONWebTokenAuthentication]
    
    def _re_map_params(self, query):
        result = {}
        query_dict = dict(query)
        print(query_dict.keys())
        for key in query_dict.keys():
            if type(query_dict.get(key)) == list:
                result[key] = query_dict.get(key).pop()
            else:
                result[key] = query_dict.get(key)        
        return result

    def get(self,request):
        try:
            param_dict = self._re_map_params(request.query_params)
            query = User.objects.only('id').get(**param_dict).id
            data_obj = Roles.objects.filter(user_id=query)
            role_serializer = RoleSerializer(data_obj,many=True)
            return Response(role_serializer.data,HTTP_201_CREATED)
        except Exception as e:
            logging.error("Exception Reached %s " % e)
            message = {
                "message" : "User not found"
            }
            return Response(message,status=HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            serializers = ApproveRoleSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=HTTP_201_CREATED)
            else:
                return Response(serializers.data,status=HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
            return Response(serializers.data,status=HTTP_417_EXPECTATION_FAILED)
