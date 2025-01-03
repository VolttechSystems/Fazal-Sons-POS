from django.urls import re_path
from AppProduct.views import *

urlpatterns = [


    ### OUTLET URL
    re_path(r'add_outlet', AddOutletView.as_view(), name='AddOutlet'),
    re_path(r'action_outlet/(?P<pk>.+)/', OutletGetView.as_view(), name='GetOutlet'),
    re_path(r'fetch_all_outlet/', FetchOutletView, name='FetchOutlet'),
    ### BRAND URL
    re_path(r'add_brand', AddBrandView.as_view(), name='AddBrand'),
    re_path(r'action_brand/(?P<pk>.+)/', BrandGetView.as_view(), name='GetBrand'),
    re_path(r'search_brand/(?P<code>.+)/', SearchBrandView, name='SearchBrand'),
    ### ATTRIBUTES TYPE URL
    re_path(r'add_attribute_type', AddAttributeTypeView.as_view(), name='AddAttributeType'),
    re_path(r'action_attribute_type/(?P<pk>.+)/', AttributeTypeGetView.as_view(), name='GetAttributeType'),
    ### ATTRIBUTES URL
    # re_path(r'add_attribute', AddAttributeView.as_view(), name='AddAttribute'),
    # re_path(r'action_attributes/(?P<pk>.+)/', AttributeGetView.as_view(), name='GetAttribute'),
    ### VARIATIONS URL
    # re_path(r'add_variation', AddVariationView.as_view(), name='AddVariation'),
    # re_path(r'add_variation', AddVariationView, name='AddVariation'),
    # re_path(r'action_variation/(?P<pk>.+)/', VariationGetView.as_view(), name='GetVariation'),
    ### HEAD CATEGORY URL
    re_path(r'add_head_category', AddHeadCategoryView.as_view(), name='AddHeadCategory'),
    re_path(r'action_head_category/(?P<pk>.+)/', HeadCategoryGetView.as_view(), name='HeadCategoryGet'),
    ### PARENT CATEGORY URL
    re_path(r'add_parent_category', AddParentCategoryView.as_view(), name='AddParentCategory'),
    re_path(r'action_parent_category/(?P<pk>.+)/', ParentCategoryGetView.as_view(), name='GetParentCategory'),
    ### CATEGORY URL
    # re_path(r'add_category', AddCategoryView.as_view(), name='AddCategory'),
    # re_path(r'action_category/(?P<pk>.+)/', CategoryGetView.as_view(), name='GetCategory'),
    ### SUB CATEGORY URL
    # re_path(r'add_subcategory', AddSubCategoryView.as_view(), name='AddSubCategory'),
    # re_path(r'action_subcategory/(?P<pk>.+)/', SubCategoryGetView.as_view(), name='GetSubCategory'),
    ### TEMPORARY PRODUCT
    re_path(r'add_temp_product', AddTemporaryProductView.as_view(), name='AddTemporaryProduct'),
    re_path(r'action_temp_product/(?P<pk>.+)/', TemporaryProductGetView.as_view(), name='GetTemporaryProduct'),
    re_path(r'all-temp-product-delete', DeleteTemporaryProductView, name='DeleteTemporaryProduct'),
    ### PRODUCT
    re_path(r'add_product', AddProduct.as_view(), name='AddProduct'),
    re_path(r'action_product/(?P<pk>.+)/', ProductGetView.as_view(), name='GetProduct'),
    re_path(r'show_product/(?P<outlet>.+)/', ShowAllProductView, name='ShowAllProduct'),
    re_path(r'shows_all_product_detail/(?P<product_id>.+)/', ShowAllProductDetailView, name='ShowAllProductDetail'),
    re_path(r'barcode_product_data/(?P<sku>.+)/', BarcodeDataView, name='BarcodeData'), ## DISPLAY THE DATA ON BARCODE
    
    ### FETCH ALL VARIATION ACCORDING TO ATTRIBUTE AND ITS TYPES
    re_path(r'fetch_all_attribute_type/', FetchAllAttributeTypeView, name='FetchAllAttributeType'),
    re_path(r'fetch_attribute/(?P<code>.+)/', FetchAttributeView, name='FetchAttributeType'),
    re_path(r'fetch_variation/(?P<code>.+)/', FetchVariationView, name='FetchAttributeName'),
    ### FETCH ALL PRODUCT NAME WITH OUTLET CODE AND STOCK 
    re_path(r'get_product/', GetAllProductView, name='GetAllProduct'),
    ### FETCH ALL CATEGORIES ACCORDING TO THEIR SUB_CATEGORIES
    re_path(r'fetch_head_to_parent_category/(?P<code>.+)/', FetchParentCategoryView, name='FetchParentCategory'),
    re_path(r'fetch_parent_to_category/(?P<code>.+)/', FetchCategoryView, name='FetchCategory'),
    re_path(r'fetch_category_to_sub_category/(?P<code>.+)/', FetchSubCategoryView, name='FetchSubCategory'),
    # VARIATION GROUP
    re_path(r'variation_group/', AddVariationGroupView, name='VariationView'),
    re_path(r'action_variations_group/(?P<att_id>.+)', GetVariationGroupView, name='GetVariation'),
    re_path(r'fetch_variations_group/(?P<att_typ_id>.+)', FetchVariationGroupView, name='FetchAttributeGroup'),
    ### NEW CATEGORY URL
    re_path(r'add_categories', AddCategoriesView, name='AddCategories'),
    re_path(r'action_categories/(?P<id>.+)', GetCategoriesView, name='GetCategories'),
    re_path(r'fetch_categories/(?P<id>.+)', FetchCategoriesView, name='FetchCategories'),
    ### NEW SUBCATEGORY URL
    re_path(r'add_subcategories', AddSubCategoriesView, name='AddSubCategories'),
    re_path(r'action_subcategories/(?P<id>.+)', GetSubCategoriesView, name='GetSubCategories'),
    re_path(r'fetch_subcategories/(?P<id>.+)', FetchSubCategoriesView, name='FetchSubCategories'),

]

## Product Edit 

