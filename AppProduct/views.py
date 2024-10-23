from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from django.http import Http404
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import connections
from rest_framework.pagination import PageNumberPagination


def DictinctFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


# FUNCTION THAT CREATE TOKEN WHEN USER IS CREATED
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


# OUTLET
class AddOutletView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


class OutletGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


# BRAND
class AddBrandView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # pagination_class = StandardResultsSetPagination


class BrandGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# ATTRIBUTES TYPE
class AddAttributeTypeView(generics.ListCreateAPIView):
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer


class AttributeTypeGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer


# ATTRIBUTES
class AddAttributeView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


# VARIATION
class AddVariationView(generics.ListCreateAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


class VariationGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


# HEAD CATEGORY
class AddHeadCategoryView(generics.ListCreateAPIView):
    queryset = HeadCategory.objects.all()
    serializer_class = HeadCategorySerializer


class HeadCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeadCategory.objects.all()
    serializer_class = HeadCategorySerializer


# PARENT CATEGORY
class AddParentCategoryView(generics.ListCreateAPIView):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer


class ParentCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer


# CATEGORY
class AddCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# SUB CATEGORY
class AddSubCategoryView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


# TEMPORARY PRODUCT
class AddTemporaryProductView(generics.ListCreateAPIView):
    queryset = TemporaryProduct.objects.all().order_by('-size')
    serializer_class = TempProductSerializer


class TemporaryProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemporaryProduct.objects.all().order_by('-size')
    serializer_class = TempProductSerializer


# PRODUCT
class AddProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# FETCH ALL VARIATION ACCORDING TO ATTRIBUTE AND ITS TYPES
@api_view(['GET'])
def FetchAllAttributeTypeView(request):
    cursor = connections['default'].cursor()
    query = "SELECT att_type from tbl_attribute_type"
    cursor.execute(query)
    all_attribute_type = DictinctFetchAll(cursor)
    return Response(all_attribute_type)


@api_view(['GET'])
def FetchAttributeView(request, code):
    cursor = connections['default'].cursor()
    query = "select attribute_name from tbl_attribute where att_type_id = '" + code + "'"
    cursor.execute(query)
    fetch_attribute = DictinctFetchAll(cursor)
    return Response(fetch_attribute)


@api_view(['GET'])
def FetchlVariationView(request, code):
    cursor = connections['default'].cursor()
    query_employee = "SELECT variation_name, symbol FROM tbl_variation where attribute_name_id = '" + code + "'"
    cursor.execute(query_employee)
    employee_location = DictinctFetchAll(cursor)
    return Response(employee_location)
