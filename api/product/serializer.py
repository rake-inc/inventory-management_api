from .models import ProductDetail
from postgres import fields
from rest_framework import serializers

PRODUCT_SERIALIZER_FIELDS = [
    fields.PRODUCT_NAME,
    fields.PRODUCT_PRICE,
    fields.PRODUCT_VENDOR,
    fields.PRODUCT_BATCH_NUMBER,
    fields.PRODUCT_QUANTITY,
    fields.PRODUCT_STATUS,
    fields.PRODUCT_BATCH_DATE,
]

PRODUCT_DISPLAY_SERIALIZER_FIELDS = [fields.PRODUCT_PK] + PRODUCT_SERIALIZER_FIELDS


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = PRODUCT_SERIALIZER_FIELDS


class ProductDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = PRODUCT_DISPLAY_SERIALIZER_FIELDS
