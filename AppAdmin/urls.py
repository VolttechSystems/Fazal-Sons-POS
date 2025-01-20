from django.urls import re_path
from .views import *

urlpatterns = [
     re_path(r'add_shop', AddShopView.as_view(), name='AddShop'),
]
