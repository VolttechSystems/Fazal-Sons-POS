from django.urls import re_path
from AppAccount.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ## LOGINS URLs
    re_path(r'auth/', obtain_auth_token, name='auth'),
    re_path(r'login', LoginAPIView.as_view(), name='LoginView'),
    re_path(r'logout', LogoutView.as_view(), name='LogoutAPI'),
    re_path(r'register_user', CreateUserView.as_view(), name='create_user'),
    re_path(r'delete_user/(?P<user_id>.+)/', UserDeleteAPIView.as_view(), name='delete_user'),
    ## SYSTEM ROLE URLS
    re_path(r'add-system-role/', AddSystemRoleView.as_view(), name='AddSystemRole'),
    # re_path(r'action-system-role', ActionSystemRoleView, name='ActionSystemRole'),
]


