from django.urls import re_path
from AppProduct.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

urlpatterns = [
    # USER URL
    re_path(r'CreateUser', CreateUserView.as_view(), name='CreateUser'),

    # AUTHENTICATION TOKEN
    # re_path(r'Generate/tokens/', obtain_auth_token, name='auth_token'),
    re_path('api-token-auth/', views.obtain_auth_token),


    # BRAND URL
    re_path(r'add_brand', AddBrandView.as_view(), name='AddBrand'),
    re_path(r'action_brand/(?P<pk>.+)/', BrandGetView.as_view(), name='GetBrand'),

    # ATTRIBUTES URL
    re_path(r'add_attribute', AddAttributeView.as_view(), name='AddAttribute'),
    re_path(r'action_attributes/(?P<pk>.+)/', AttributeGetView.as_view(), name='GetAttribute'),

    # VARAITIONS URL
    re_path(r'add_variation', AddVariationView.as_view(), name='AddVariation'),
    re_path(r'action_variation/(?P<pk>.+)/', VariationGetView.as_view(), name='GetVariation'),

    # PARENT CATEGORY URL
    re_path(r'add_parent_category', AddParentCategoryView.as_view(), name='AddParentCategory'),
    re_path(r'action_parent_category/(?P<pk>.+)/', ParentCategoryGetView.as_view(), name='GetParentCategory'),

    # CATEGORY URL
    re_path(r'add_category', AddCategoryView.as_view(), name='AddCategory'),
    re_path(r'action_category/(?P<pk>.+)/', CategoryGetView.as_view(), name='GetCategory'),

    # SUB CATEGORY URL
    re_path(r'add_subcategory', AddSubCategoryView.as_view(), name='AddSubCategory'),
    re_path(r'action_subcategory/(?P<pk>.+)/', SubCategoryGetView.as_view(), name='GetSubCategory'),

    # PRODUCT
    re_path(r'add_product', AddProduct.as_view(), name='AddProduct'),
    re_path(r'action_product/(?P<pk>.+)/', ProductGetView.as_view(), name='GetProduct'),

]
