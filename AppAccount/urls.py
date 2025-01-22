from django.urls import re_path
from AppAccount.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ## LOGINS URLs
    re_path(r'auth/', obtain_auth_token, name='auth'),
    re_path(r'login', LoginAPIView.as_view(), name='LoginView'),
    re_path(r'logout', LogoutView.as_view(), name='LogoutAPI'),
    re_path(r'register_user/(?P<shop>.+)', CreateUserView, name='create_user'),
    re_path(r'delete_user/(?P<user_id>.+)', UserDeleteAPIView.as_view(), name='delete_user'),
    re_path(r'admin-change-password/', AdminChangePasswordView.as_view(), name='admin-change-password'),
    ## SYSTEM ROLE URLS
    re_path(r'get-all-permissions', GetPermissionsView, name='GetPermissions'),
    re_path(r'add-system-role/(?P<shop>.+)', AddSystemRoleView, name='AddSystemRole'),
    re_path(r'action-system-role/(?P<shop>.+)/(?P<pk>.+)/', ActionSystemRoleView.as_view(), name='ActionSystemRole'),
    re_path(r'fetch-system-role/(?P<shop>.+)', FetchSystemRoleView, name='FetchSystemRole'),
]


