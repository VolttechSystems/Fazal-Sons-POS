from django.urls import re_path
from .views import *

urlpatterns = [
     re_path(r'add_shop', AddShopView.as_view(), name='AddShop'),
     re_path(r'shop-admin-user', ShopAdminUserView, name='ShopAdminUser'),
]
