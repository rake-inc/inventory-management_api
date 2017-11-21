from rest_framework.views import APIView
from django.auth.contrib.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ProductDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        pass

    def post(self, request):
        pass

    def update(self, request):
        pass

    def delete(self, request):
        pass
