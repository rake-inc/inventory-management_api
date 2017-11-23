from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^create-user/$', views.CreateUser.as_view(), name='user-creation'),
    url(r'^role/$', views.RoleDetails.as_view(), name='user-role-details'),
    url(r'^role-approval/(?P<pk>[0-9]+)/$', views.RoleApprovalDetail.as_view(), name='role-approval-details'),
]
