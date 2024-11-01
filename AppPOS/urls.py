from django.urls import re_path
from .views import*


urlpatterns = [
        re_path(r'add_transaction', AddTransactionView.as_view(), name='AddTransaction'),
     
]
