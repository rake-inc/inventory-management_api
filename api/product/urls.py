from django.conf.urls import url
from .views import ProductDetailAPI

urlpatterns = [
    url(r'^product-api/$', ProductDetailAPI.as_view()),
]
