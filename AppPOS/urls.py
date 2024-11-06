from django.urls import re_path
from .views import*


urlpatterns = [
        re_path(r'add_transaction', AddTransactionView.as_view(), name='AddTransaction'),
        re_path(r'add_additional_fee', AddAdditionalFeeView.as_view(), name='AddAdditionalFee'),
        re_path(r'action_additional_fee/(?P<pk>.+)/', GetAdditionalFeeView.as_view(), name='GetAdditionalFee'),
]
