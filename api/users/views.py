from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer, RoleSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED


# Create your views here.

class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def _re_map_roles(self, serializer):
        result = {}
        if len(serializer):
            return {'1': serializer}

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        r_data = {}
        try:
            r_data.update(store_manager=request.data.pop("store_manager"))
            r_data.update(department_manager=request.data.pop("department_manager"))
            if user_serializer.is_valid():
                user_serializer.save()
            _id = User.objects.only('id').get(username=request.data.get("username")).id
            # print (_id)
            r_data.update(user_id=_id)
            processed_role_data = self.remap(r_data)
            role_serializer = RoleSerializer(data=processed_role_data)
            if role_serializer.is_valid():
                role_serializer.save()
            return Response(user_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            print e
        return Response(user_serializer.errors, status=HTTP_417_EXPECTATION_FAILED)
