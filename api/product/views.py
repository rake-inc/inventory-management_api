import logging
from utils import mapper
from postgres import fields
from .models import ProductDetails
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer, ProductDisplaySerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_200_OK, HTTP_400_BAD_REQUEST


class ProductDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def _paginated_model_instance(self, query):
        """
        Paginating the product entities based on the start and end limits specified
        :param query:
        :return:
        """
        paginated_obj = ProductDetails.objects.all()[query.get(fields.START):query.get(fields.END)]
        return paginated_obj

    def get(self, request):
        """
        GET method for accessing the product details
        :param request:
        :return:
        """
        try:
            remapped_query = mapper.re_map_role_params(request.data)
            query_obj = self._paginated_model_instance(remapped_query)
            product_display_serializer = ProductDisplaySerializer(query_obj)
            return Response(data=product_display_serializer.data, status=HTTP_200_OK)
        except Exception as e:
            logging.error("EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        POST method for adding a new product record to the database
        :param request:
        :return:
        """
        try:
            product_serializer = ProductSerializer(request.data)
            if product_serializer.is_valid():
                logging.info("PRODUCT RECORD ADDED SUCCESSFULLY")
                return Response(product_serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            logging.error("EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)

    def put(self, request):
        """
        PUT method for updating the existing product record. Record can be pointed by querying the primary key
        :param request:
        :return:
        """
        try:
            pk, query = mapper.re_map_update_query(request.data)
            ProductDetails.objects.filter(pk=pk).update(**query)
            return Response(status=HTTP_200_OK)
        except Exception as e:
            logging.error("EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)

    def delete(self, request):
        """
        DELETE method for deleting a product record from the database based on a unique key specified
        :param request:
        :return:
        """
        try:
            remapped_query = mapper.re_map_role_params(request.data)
            ProductDetails.objects.filter(**remapped_query).delete()
            return Response(status=HTTP_200_OK)
        except Exception as e:
            logging.error("EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)
