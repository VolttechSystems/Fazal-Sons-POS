from django.urls import re_path
from AppProduct.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

urlpatterns = [
    # USER URL

    # AUTHENTICATION TOKEN
    # re_path(r'Generate/tokens/', obtain_auth_token, name='auth_token'),
    re_path('api-token-auth/', views.obtain_auth_token),

    # OUTLET URL
    re_path(r'add_outlet', AddOutletView.as_view(), name='AddOutlet'),
    re_path(r'action_outlet/(?P<pk>.+)/', OutletGetView.as_view(), name='GetOutlet'),

    # BRAND URL
    re_path(r'add_brand', AddBrandView.as_view(), name='AddBrand'),
    re_path(r'action_brand/(?P<pk>.+)/', BrandGetView.as_view(), name='GetBrand'),

    # ATTRIBUTES TYPE URL
    re_path(r'add_attribute_type', AddAttributeTypeView.as_view(), name='AddAttributeType'),
    re_path(r'action_attribute_type/(?P<pk>.+)/', AttributeTypeGetView.as_view(), name='GetAttributeType'),

    # ATTRIBUTES URL
    re_path(r'add_attribute', AddAttributeView.as_view(), name='AddAttribute'),
    re_path(r'action_attributes/(?P<pk>.+)/', AttributeGetView.as_view(), name='GetAttribute'),

    # VARAITIONS URL
    re_path(r'add_variation', AddVariationView.as_view(), name='AddVariation'),
    re_path(r'action_variation/(?P<pk>.+)/', VariationGetView.as_view(), name='GetVariation'),

    # HEAD CATEGORY URL
    re_path(r'add_head_category', AddHeadCategoryView.as_view(), name='AddHeadCategory'),
    re_path(r'action_head_category/(?P<pk>.+)/', HeadCategoryGetView.as_view(), name='HeadCategoryGet'),

    # PARENT CATEGORY URL
    re_path(r'add_parent_category', AddParentCategoryView.as_view(), name='AddParentCategory'),
    re_path(r'action_parent_category/(?P<pk>.+)/', ParentCategoryGetView.as_view(), name='GetParentCategory'),

    # CATEGORY URL
    re_path(r'add_category', AddCategoryView.as_view(), name='AddCategory'),
    re_path(r'action_category/(?P<pk>.+)/', CategoryGetView.as_view(), name='GetCategory'),

    # SUB CATEGORY URL
    re_path(r'add_subcategory', AddSubCategoryView.as_view(), name='AddSubCategory'),
    re_path(r'action_subcategory/(?P<pk>.+)/', SubCategoryGetView.as_view(), name='GetSubCategory'),

    # TEMPORARY PRODUCT
    re_path(r'get_temp_product', GetTemporaryProductView, name='FetchTemporaryProduct'),
    re_path(r'add_temp_product', AddTemporaryProductView.as_view(), name='AddTemporaryProduct'),
    re_path(r'action_temp_product/(?P<pk>.+)/', TemporaryProductGetView.as_view(), name='GetTemporaryProduct'),

    # PRODUCT
    re_path(r'add_product', AddProduct.as_view(), name='AddProduct'),
    re_path(r'action_product/(?P<pk>.+)/', ProductGetView.as_view(), name='GetProduct'),

    # FETCH ALL VARIATION ACCORDING TO ATTRIBUTE AND ITS TYPES
    re_path(r'fetch_all_attribute_type/', FetchAllAttributeTypeView, name='FetchAllAttributeType'),
    re_path(r'fetch_attribute/(?P<code>.+)/', FetchAttributeView, name='FetchAttributeType'),
    re_path(r'fetch_variation/(?P<code>.+)/', FetchlVariationView, name='FetchAttributeName'),

]
