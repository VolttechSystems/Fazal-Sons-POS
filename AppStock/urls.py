from django.urls import re_path
from AppStock.views import *

urlpatterns = [
    ### UPDATE STOCK URL 
    re_path(r'add_stock/(?P<code>.+)/', AddStockView, name='AddStock'),
]
