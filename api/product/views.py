import logging
from utils import mapper
from postgres import fields
from .models import ProductDetail
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer, ProductDisplaySerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.status import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_200_OK, HTTP_400_BAD_REQUEST


class ProductDetailAPI(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def _paginated_model_instance(self, query):
        """
        Paginating the product entities based on the start and end limits specified
        :param query:
        :return:
        """
        paginated_obj = ProductDetail.objects.all().order_by(fields.PRODUCT_PK)[
                        int(query.get(fields.START)):int(query.get(fields.END))]
        return paginated_obj

    def _str_to_int(self, query_dict):
        """
        converts string values to integer
        :param query_dict:
        :return:
        """
        for key in query_dict.keys():
            query_dict[key] = int(query_dict.get(key))
        return query_dict

    def _get_product_count(self):
        """
        Returns the total number of product entities
        :return:
        """
        return ProductDetail.objects.count()

    def get(self, request):
        """
        GET method for accessing the product details
        :param request:
        :return:
        """
        try:
            if fields.TOTAL_PRODUCTS in request.query_params.keys():
                return Response(data=self._get_product_count(), status=HTTP_200_OK)
            remapped_query = mapper.re_map_role_params(request.query_params)
            query_dict = self._str_to_int(remapped_query)
            query_obj = self._paginated_model_instance(query_dict)
            product_display_serializer = ProductDisplaySerializer(query_obj, many=True)
            if len(product_display_serializer.data) == 0:
                return Response(data={}, status=HTTP_200_OK)
            return Response(data=product_display_serializer.data, status=HTTP_200_OK)
        except Exception as e:
            logging.error("ProductDetail GET EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        POST method for adding a new product record to the database
        :param request:
        :return:
        """
        try:
            product_serializer = ProductSerializer(data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                logging.info("PRODUCT RECORD ADDED SUCCESSFULLY")
                return Response(data=product_serializer.data, status=HTTP_201_CREATED)
            return Response(product_serializer.errors, status=HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            logging.error("ProductDetail POST EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)

    def put(self, request):
        """
        PUT method for updating the existing product record. Record can be pointed by querying the primary key
        :param request:
        :return:
        """
        try:
            pk_dict, query = mapper.re_map_update_query(request.data)
            pk = self._str_to_int(pk_dict)
            ProductDetail.objects.filter(**pk).update(**query)
            return Response(status=HTTP_200_OK)
        except Exception as e:
            logging.error("ProductDetail PUT EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)

    def delete(self, request):
        """
        DELETE method for deleting a product record from the database based on a unique key specified
        :param request:
        :return:
        """
        try:
            remapped_query = mapper.re_map_role_params(request.query_params)
            ProductDetail.objects.filter(**remapped_query).delete()
            return Response(status=HTTP_200_OK)
        except Exception as e:
            logging.error("ProductDetail DELETE EXCEPTION REACHED %s" % e)
            return Response(status=HTTP_417_EXPECTATION_FAILED)
