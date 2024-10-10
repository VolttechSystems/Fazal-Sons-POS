from django.urls import re_path
from AppCustomer.views import *


urlpatterns = [
    # CUSTOMER CHANNEL URL
    re_path(r'add_customer_channel', AddCustomerChannel.as_view(), name='AddCustomerChannel'),
    re_path(r'action_customer_channel/(?P<pk>.+)/', GetCustomerChannel.as_view(), name='GetCustomerChannel'),

    # CUSTOMER TYPE URL
    re_path(r'add_customer_type', AddCustomerType.as_view(), name='AddCustomerType'),
    re_path(r'action_customer_type/(?P<pk>.+)/', GetCustomerType.as_view(), name='GetCustomerType'),

    # CUSTOMER URL
    re_path(r'add_customer', AddCustomer.as_view(), name='AddCustomer'),
    re_path(r'action_customer/(?P<pk>.+)/', GetCustomer.as_view(), name='GetCustomer'),
]