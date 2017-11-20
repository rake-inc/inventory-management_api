from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^create-user/$', views.CreateUser.as_view()),
    url(r'^role/$',views.RoleDetails.as_view()),
]
