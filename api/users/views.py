import logging
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer, RoleSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED


# Create your views here.

class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        r_data = {}
        print (request.data)
        try:
            user_serializer = UserSerializer(data=request.data)
            r_data.update(store_manager=request.data.pop("store_manager"))
            r_data.update(department_manager=request.data.pop("department_manager"))
            print(r_data)
            if user_serializer.is_valid():
                user_serializer.save()
            _id = User.objects.only('id').get(username=request.data.get("username")).id
            logging.info("User created with ID %s" %_id)
            r_data.update(user_id=_id)
            processed_role_data = self._re_map_roles(r_data)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            logging.error("Exception Reached %s" % e)
        return Response(status=HTTP_417_EXPECTATION_FAILED)

    def _re_map_roles(self, serializer):
        result = {}
        if len(serializer):
            result['store_manager'] = bool(serializer.get('store_manager'))
            result['department_manager'] = bool(serializer.get('department_manager'))
            result['user'] = serializer.get('user_id')
        return result