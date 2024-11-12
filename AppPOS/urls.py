from django.urls import re_path
from .views import*


urlpatterns = [
        ### TRANSACTION URL
        re_path(r'add_transaction', AddTransactionView.as_view(), name='AddTransaction'),
        ### ADDITIONAL FEE URL
        re_path(r'add_additional_fee', AddAdditionalFeeView.as_view(), name='AddAdditionalFee'),
        re_path(r'action_additional_fee/(?P<pk>.+)/', GetAdditionalFeeView.as_view(), name='GetAdditionalFee'),
        ### SALESMAN URL
        re_path(r'add_salesman', AddSalesmanView.as_view(), name='AddSalesman'),
        re_path(r'action_salesman/(?P<pk>.+)/', GetSalesmanView.as_view(), name='GetSalesman'),
]
