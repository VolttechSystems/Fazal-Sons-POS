from django.urls import re_path
from AppAccount.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    re_path('auth/', obtain_auth_token, name='auth'),

    # re_path('login', LoginAPIView.as_view(), name='LoginView'),
    re_path('logout', LogoutView.as_view(), name='LogoutAPI'),
    re_path(r'register_user', CreateUserView.as_view(), name='CreateUser'),



]

