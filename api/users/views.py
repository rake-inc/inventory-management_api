from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED


# Create your views here.

class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            print(type(request.data))
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response(serializer.errors, status=HTTP_417_EXPECTATION_FAILED)


class CreateRole(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        pass
