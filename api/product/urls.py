from django.conf.urls import url
from .views import ProductDetail

urlpatterns = [
    url(r'^product-api/$', ProductDetail.as_view()),
]
