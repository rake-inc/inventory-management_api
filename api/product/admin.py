from django.contrib import admin
from .models import ProductDetail
from postgres import fields

# Register your models here.

PRODUCT_DETAILS_ADMIN_FIELDS = [
    fields.PRODUCT_PK,
    fields.PRODUCT_NAME,
    fields.PRODUCT_PRICE,
    fields.PRODUCT_VENDOR,
    fields.PRODUCT_BATCH_NUMBER,
    fields.PRODUCT_QUANTITY,
    fields.PRODUCT_STATUS,
    fields.PRODUCT_BATCH_DATE,

]


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = PRODUCT_DETAILS_ADMIN_FIELDS


admin.site.register(ProductDetail, ProductDetailAdmin)
