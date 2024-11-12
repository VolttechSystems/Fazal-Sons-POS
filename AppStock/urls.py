from django.urls import re_path
from AppStock.views import *

urlpatterns = [
    ### UPDATE STOCK URL 
    re_path(r'add_stock/', AddStockView, name='AddStock'),
]
