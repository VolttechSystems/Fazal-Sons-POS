from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.db import connections
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from AppCustomer.utils import DistinctFetchAll
from django.db.models import Prefetch
from rest_framework.exceptions import NotFound

### FUNCTION THAT CREATE TOKEN WHEN USER IS CREATED
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


### CUSTOM PAGINATION CLASS
class MyLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = "limit"
    offset_query_param = "Starting"


### OUTLET VIEW
class AddOutletView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = OutletSerializer
    pagination_class = None
    
    def get_queryset(self):
        # Access the 'shop' parameter from the URL
        shop_id = self.kwargs.get('shop')
        return Outlet.objects.filter(shop_id=shop_id).order_by("id")
        
        
class OutletGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outlet.objects.all().order_by("id")
    serializer_class = OutletSerializer
    pagination_class = None
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        return Outlet.objects.filter(shop_id=shop_id).order_by("id")
        

@api_view(["GET"])
def FetchOutletView(request, shop):
    outlets = Outlet.objects.filter(shop_id=shop)
    if outlets.exists():
        serializer = OutletSerializer(outlets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def SyncOutlets(request):
    outlets = request.data
    try:
        for outlet in outlets:
            # Insert or update each outlet
            Outlet.objects.update_or_create(
                outlet_code=outlet['outlet_code'],
                defaults={'outlet_name': outlet['outlet_name']}
            )
        return Response({'message': 'Data synced successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error syncing outlets: {e}")
        return Response({'error': 'Error syncing outlets'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### BRAND VIEW
class AddBrandView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BrandSerializer
    pagination_class = MyLimitOffsetPagination
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        brand = Brand.objects.filter(shop_id=shop_id)
        return brand
        

class BrandGetView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandSerializer
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        brand = Brand.objects.filter(shop_id=shop_id)
        return brand
    

@api_view(["GET"])
def SearchBrandView(request, shop, code):
    brand_name = code
    brand = Brand.objects.filter(shop_id=shop, brand_name__icontains=brand_name).order_by(
        "id"
    )
    if len(brand) > 0:
        serializer = BrandSerializer(brand, many=True)
        param = {
            "status": 200,
            "results": serializer.data,
        }
        return Response(param)
    return Response(status=status.HTTP_204_NO_CONTENT)


### ATTRIBUTES TYPE VIEW
class AddAttributeTypeView(generics.ListCreateAPIView):
    serializer_class = AttributeTypeSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = AttributeType.objects.filter(shop_id=get_shop).order_by("id")
        return queryset
        

class AttributeTypeGetView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttributeTypeSerializer
    pagination_class = None
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = AttributeType.objects.filter(shop_id=get_shop).order_by("id")
        return queryset
        
        
#### VARIATION GROUP VIEW
@api_view(["GET", "POST"])
def AddVariationGroupView(request, shop):
    if request.method == "GET":
        array = []
        attribute_type = AttributeType.objects.filter(shop_id=shop)
        for i in range(len(attribute_type)):
            att_type = attribute_type[i].att_type
            att_type_id = attribute_type[i].id

            attribute = Attribute.objects.filter(shop_id=shop,att_type_id=att_type_id)
            if len(attribute) > 0:
                for i in range(len(attribute)):
                    att_name = attribute[i].attribute_name
                    att_id = attribute[i].id
                    attribute_name_id = attribute[i].id

                    variation = Variation.objects.filter(
                        shop_id=shop,
                        attribute_name=attribute_name_id
                    )
                    if len(variation) > 0:
                        variation_name = []
                        for i in range(len(variation)):
                            variation_name.append(variation[i].variation_name)
                        Dict = dict()
                        Dict["att_id"] = att_id
                        Dict["att_type"] = att_type
                        Dict["attribute_name"] = att_name
                        Dict["variation"] = variation_name
                        array.append(Dict)
                    elif len(variation) == 0:
                        Dict = dict()
                        Dict["att_id"] = att_id
                        Dict["att_type"] = att_type
                        Dict["attribute_name"] = att_name
                        Dict["variation"] = None
                        array.append(Dict)
        paginator = LimitOffsetPagination()
        paginated_variation_group = paginator.paginate_queryset(array, request)
        return paginator.get_paginated_response(paginated_variation_group)
    if request.method == "POST":
        data = request.data
        for i in range(len(data)):
            serializer = VariationGroupSerializer(data=request.data[i], context={'request': request})
            if serializer.is_valid():
                serializer.save()
        return Response(data, status="200")


@api_view(["GET", "PUT", "DELETE"])
def GetVariationGroupView(request, shop, att_id):
    if request.method == "GET":
        array = []
        try:
            attribute = Attribute.objects.get(shop_id=shop, id=att_id)
            attribute_type = AttributeType.objects.get(shop_id=shop, id=attribute.att_type_id)
        except:
            return Response("NO RECORD FOUND")
        att_type = attribute_type.att_type
        att_type_id = attribute_type.id
        att_name = attribute.attribute_name
        attribute_name_id = attribute.id

        variation = Variation.objects.filter(shop_id=shop, attribute_name=attribute_name_id)
        if len(variation) > 0:
            variation_name = []
            for i in range(len(variation)):
                variation_name.append(variation[i].variation_name)
            Dict = dict()
            Dict["att_id"] = att_id
            Dict["att_type"] = att_type
            Dict["attribute_name"] = att_name
            Dict["variation_name"] = variation_name
            array.append(Dict)
        elif len(variation) == 0:
            Dict = dict()
            Dict["att_id"] = att_id
            Dict["att_type"] = att_type
            Dict["attribute_name"] = att_name
            Dict["variation_name"] = None
            array.append(Dict)
        return Response(array)
    
    elif request.method == "PUT":
        data = request.data
        id = data["att_id"]
        try:
            attribute = Attribute.objects.get(shop_id=shop, id=id)
        except:
            return Response("NO RECORD FOUND")
        attribute.attribute_name = data["attribute_name"]
        attribute.att_type_id = data["att_type"]
        attribute.save()
        variation = Variation.objects.filter(shop_id=shop, attribute_name=att_id)
        if len(variation) == len(data["variation_name"]):
            for i in range(len(variation)):
                variation[i].variation_name = data["variation_name"][i]
                variation[i].save()
        elif len(variation) != len(data["variation_name"]):
            if len(variation) > 0:
                for i in range(len(variation)):
                    variation[i].delete()
                for y in range(len(data["variation_name"])):
                    variation = Variation()
                    variation.variation_name = data["variation_name"][y]
                    variation.attribute_name_id = data["att_id"]
                    variation.status = "active"
                    variation.created_at = datetime.datetime.now()
                    variation.save()
            else:
                for y in range(len(data["variation_name"])):
                    variation = Variation()
                    variation.variation_name = data["variation_name"][y]
                    variation.attribute_name_id = data["att_id"]
                    variation.status = "active"
                    variation.created_at = datetime.datetime.now()
                    variation.save()
        return Response(data)
    elif request.method == "DELETE":
        attribute = Attribute.objects.get(shop_id=shop, id=att_id)
        variation = Variation.objects.filter(shop_id=shop, attribute_name_id=att_id)
        for i in range(len(variation)):
            variation[i].delete()
        attribute.delete()
        attribute_type = Attribute.objects.filter(shop_id=shop, att_type_id=attribute.att_type_id)
        if len(attribute_type) == 0:
            attribute_type = AttributeType.objects.get(shop_id=shop, id=attribute.att_type_id)
            attribute_type.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def FetchVariationGroupView(request, shop, att_typ_id):
    if request.method == "GET":
        att_id = att_typ_id
        array = []
        try:
            attribute_type = AttributeType.objects.get(shop_id=shop, id=att_id)
            attribute = Attribute.objects.filter(shop_id=shop, att_type=attribute_type.id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for i in range(len(attribute)):
            att_type = attribute_type.att_type
            att_type_id = attribute_type.id
            att_name = attribute[i].attribute_name
            attribute_id = attribute[i].id
            attribute_name_id = attribute[i].id

            variation = Variation.objects.filter(shop_id=shop, attribute_name=attribute_name_id)
            if len(variation) > 0:
                variation_name = []
                for i in range(len(variation)):
                    variation_name.append(variation[i].variation_name)
                Dict = dict()
                Dict["att_id"] = att_id
                Dict["att_type"] = att_type
                Dict["attribute_name"] = att_name
                Dict["attribute_id"] = attribute_id
                Dict["variation"] = variation_name
                array.append(Dict)
            elif len(variation) == 0:
                Dict = dict()
                Dict["att_id"] = att_id
                Dict["att_type"] = att_type
                Dict["attribute_name"] = att_name
                Dict["attribute_id"] = attribute_id
                Dict["variation"] = None
                array.append(Dict)
        return Response(array)


### HEAD CATEGORY VIEW
class AddHeadCategoryView(generics.ListCreateAPIView):
    serializer_class = HeadCategorySerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = HeadCategory.objects.filter(shop_id=get_shop).order_by("id")
        return queryset


class HeadCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HeadCategorySerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = HeadCategory.objects.filter(shop_id=get_shop).order_by("id")
        return queryset


### PARENT CATEGORY VIEW
class AddParentCategoryView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ParentCategorySerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = ParentCategory.objects.filter(shop_id=get_shop).order_by("id")
        return queryset

class ParentCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParentCategorySerializer
    pagination_class = None
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = ParentCategory.objects.filter(shop_id=get_shop).order_by("id")
        return queryset
    
### CATEGORY VIEW
@api_view(["GET", "POST"])
def AddCategoriesView(request, shop):
    if request.method == "GET":
        cursor = connections["default"].cursor()
        query = "Select  ca.shop_id, ca.id, category_name, ca.symbol, subcategory_option, ca.description, ca.status, pc_name from tbl_category ca inner join tbl_parent_category pc on ca.pc_name_id = pc.id WHERE ca.shop_id = '" + shop +"'"
        cursor.execute(query)
        variation_group = DistinctFetchAll(cursor)
        variation_array = []
        if len(variation_group) > 0:
            for i in range(len(variation_group)):
                variation_dict = dict()
                variation_dict["id"] = variation_group[i]["id"]
                variation_dict["category_name"] = variation_group[i]["category_name"]
                variation_dict["symbol"] = variation_group[i]["symbol"]
                variation_dict["subcategory_option"] = variation_group[i][
                    "subcategory_option"
                ]
                variation_dict["description"] = variation_group[i]["description"]
                variation_dict["status"] = variation_group[i]["status"]
                variation_dict["pc_name"] = variation_group[i]["pc_name"]
                category_attribute = CategoryAttribute.objects.filter(
                    category_id=variation_group[i]["id"]
                )
                attribute_group_array = []
                if len(category_attribute) > 0:
                    for i in range(len(category_attribute)):
                        attribute = Attribute.objects.get(
                            shop_id=shop,
                            id=category_attribute[i].attribute_id
                        ).attribute_name
                        attribute_group_array.append(attribute)
                variation_dict["attribute_group"] = attribute_group_array
                variation_dict["shop"] = variation_group[i]["shop_id"]
                variation_array.append(variation_dict)
        paginator = LimitOffsetPagination()
        paginated_category = paginator.paginate_queryset(variation_array, request)
        return paginator.get_paginated_response(paginated_category)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            category_array = []
            category_dict = dict()
            category_name = request.data["category_name"].strip()
            category = Category.objects.get(category_name=category_name)
            category_dict["id"] = category.id
            category_dict["pc_name"] = category.pc_name_id
            category_dict["category_name"] = category.category_name
            category_dict["symbol"] = category.symbol
            category_dict["description"] = category.description
            category_dict["status"] = category.status
            attribute_group_array = []
            category_attribute = CategoryAttribute.objects.filter(
                category_id=category.id
            )
            if len(category_attribute) > 0:
                for i in range(len(category_attribute)):
                    attribute = Attribute.objects.get(
                        id=category_attribute[i].attribute_id
                    ).attribute_name
                    attribute_group_array.append(attribute)
            category_dict["attribute_group"] = attribute_group_array
            category_array.append(category_dict)
            return Response(category_array)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def GetCategoriesView(request, shop, id):
    try:
        category = Category.objects.get(shop_id=shop, id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        cursor = connections["default"].cursor()
        query = (
            "Select ca.id, category_name, ca.symbol, subcategory_option, ca.description, ca.status, pc_name, pc.id as parent_id, hc.id as head_id, hc_name as head_name, pc_name as parent_name from tbl_category ca inner join tbl_parent_category pc on ca.pc_name_id = pc.id inner join tbl_head_category hc on pc.hc_name_id = hc.id where ca.id = '"+ id +"' and ca.shop_id = '"+ shop +"'"
        )
        cursor.execute(query)
        variation_group = DistinctFetchAll(cursor)
        if not variation_group:
            return Response(status=404)
        
        # Build the response using the first item
        variation_data = variation_group[0]

        variation_dict = dict()
        variation_dict["id"] = variation_data["id"]
        variation_dict["head_id"] = variation_data["head_id"]
        variation_dict["head_name"] = variation_data["head_name"]
        variation_dict["parent_id"] = variation_data["parent_id"]
        variation_dict["parent_name"] = variation_data["parent_name"]
        variation_dict["category_name"] = variation_data["category_name"]
        variation_dict["symbol"] = variation_data["symbol"]
        variation_dict["subcategory_option"] = variation_data["subcategory_option"]
        variation_dict["description"] = variation_data["description"]
        variation_dict["status"] = variation_data["status"]
        variation_dict["pc_name"] = variation_data["pc_name"]
        category_attribute = CategoryAttribute.objects.filter(category_id=id)
 
        attribute_group_array = []
        attribute_type_array = []

        if category_attribute:
            # Fetch all attribute IDs in a single query
            attribute_ids = [item.attribute_id for item in category_attribute]
            attributes = Attribute.objects.filter(id__in=attribute_ids).select_related('att_type')

            # Iterate through fetched attributes
            for attribute in attributes:
                # Add to attribute group array
                attribute_group_array.append({
                    "att_type": attribute.att_type_id,
                    "att_type_name": attribute.att_type.att_type,
                    "id": attribute.id,
                    "name": attribute.attribute_name,
                })
                # Add to attribute type array
                if attribute.att_type:
                    attribute_type_array.append({
                        "id": attribute.att_type_id,
                        "name": attribute.att_type.att_type,
                
              })

        variation_dict["attribute_group"] = attribute_group_array
        variation_dict["att_type"] = attribute_type_array
        return Response(variation_dict)

    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def FetchCategoriesView(request, shop, id):
    if request.method == "GET":
        try:
            category = Category.objects.get(shop_id=shop, id=id)
        except Category.DoesNotExist:
                 return Response(status=status.HTTP_404_NOT_FOUND)

        category_attribute = CategoryAttribute.objects.filter(category_id=category.id)
        cat_array = []
        if len(category_attribute) > 0:
            for i in range(len(category_attribute)):
                try:
                    attribute = Attribute.objects.get(
                        shop_id=shop,
                        id=category_attribute[i].attribute_id
                    )
                except:
                    return Response("Attribute not found against this category")

                variation = Variation.objects.filter(shop_id=shop, attribute_name_id=attribute.id)
                if len(variation) > 0:
                    cat_dict = dict()
                    cat_dict["id"] = category.id
                    cat_dict["category"] = category.category_name
                    cat_dict["attribute"] = attribute.attribute_name
                    cat_dict["shop"] = category.shop_id
                    variation_array = []
                    for x in range(len(variation)):
                        variation_array.append(variation[x].variation_name)
                        cat_dict["variation"] = variation_array
                    cat_array.append(cat_dict)
        return Response(cat_array)

### SUBCATEGORY VIEW
@api_view(["GET", "POST"])
def AddSubCategoriesView(request, shop):
    if request.method == "GET":
        sub_category = SubCategory.objects.filter(shop_id=shop)
        sub_category_array = []
        if len(sub_category) > 0:
            for i in range(len(sub_category)):
                sub_category_dict = dict()
                sub_category_dict["id"] = sub_category[i].id
                sub_category_dict["sub_category_name"] = sub_category[
                    i
                ].sub_category_name
                sub_category_dict["symbol"] = sub_category[i].symbol
                sub_category_dict["description"] = sub_category[i].description
                sub_category_dict["status"] = sub_category[i].status

                if  sub_category[i].category_id != None:
                    sub_category_dict["category"] = sub_category[i].category.category_name
                else:
                    sub_category_dict["category"] = None

                sub_category_attribute = SubCategoryAttribute.objects.filter(
                    sub_category_id=sub_category[i].id
                )
                attribute_group_array = []
                if len(sub_category_attribute) > 0:
                    for i in range(len(sub_category_attribute)):
                        attribute = Attribute.objects.get(
                            shop_id=shop,
                            id=sub_category_attribute[i].attribute_id
                        ).attribute_name
                        attribute_group_array.append(attribute)
                sub_category_dict["attribute_group"] = attribute_group_array
                sub_category_array.append(sub_category_dict)
        paginator = LimitOffsetPagination()
        paginated_sub_category = paginator.paginate_queryset(sub_category_array, request)
        return paginator.get_paginated_response(paginated_sub_category)
    elif request.method == "POST":
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sub_category_array = []
            sub_category_dict = dict()
            sub_category_name = request.data["sub_category_name"].strip()
            sub_category = SubCategory.objects.get(sub_category_name=sub_category_name)
            sub_category_dict["id"] = sub_category.id
            sub_category_dict["category"] = sub_category.category_id
            sub_category_dict["sub_category_name"] = sub_category.sub_category_name
            sub_category_dict["symbol"] = sub_category.symbol
            sub_category_dict["description"] = sub_category.description
            sub_category_dict["status"] = sub_category.status
            attribute_group_array = []
            sub_category_attribute = SubCategoryAttribute.objects.filter(
                sub_category_id=sub_category.id
            )
            if len(sub_category_attribute) > 0:
                for i in range(len(sub_category_attribute)):
                    attribute = Attribute.objects.get(
                        shop_id=shop,
                        id=sub_category_attribute[i].attribute_id
                    ).attribute_name
                    attribute_group_array.append(attribute)
            sub_category_dict["attribute_group"] = attribute_group_array
            sub_category_array.append(sub_category_dict)
            return Response(sub_category_array)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def GetSubCategoriesView(request, shop, id):
    try:
        sub_category = SubCategory.objects.select_related("category").get(shop_id=shop, id=id)
    except SubCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        sub_category_dict = dict()
        sub_category_dict["id"] = sub_category.id
        sub_category_dict["head_id"] = sub_category.category.pc_name.hc_name.id
        sub_category_dict["head_name"] = sub_category.category.pc_name.hc_name.hc_name
        sub_category_dict["parent_id"] = sub_category.category.pc_name.id
        sub_category_dict["parent_name"] = sub_category.category.pc_name.pc_name
        sub_category_dict["category_id"] = sub_category.category.id
        sub_category_dict["category_name"] = sub_category.category.category_name
        sub_category_dict["sub_category_name"] = sub_category.sub_category_name
        sub_category_dict["symbol"] = sub_category.symbol
        sub_category_dict["description"] = sub_category.description
        sub_category_dict["status"] = sub_category.status
     
        sub_category_attribute = SubCategoryAttribute.objects.filter(
            sub_category_id=sub_category.id
        )
        attribute_group_array = []
        attribute_type_array = []
        if sub_category_attribute:
            # Fetch all attribute IDs in a single query
            attribute_ids = [item.attribute_id for item in sub_category_attribute]
            attributes = Attribute.objects.filter(id__in=attribute_ids).select_related('att_type')

            # Iterate through fetched attributes
            for attribute in attributes:
                # Add to attribute group array
                attribute_group_array.append({
                    "att_type": attribute.att_type_id,
                    "att_type_name": attribute.att_type.att_type,
                    "id": attribute.id,
                    "name": attribute.attribute_name,
                })
                # Add to attribute type array
                if attribute.att_type:
                    attribute_type_array.append({
                        "id": attribute.att_type_id,
                        "name": attribute.att_type.att_type,
              })
        sub_category_dict["attribute_group"] = attribute_group_array
        sub_category_dict["att_type"] = attribute_type_array
        return Response(sub_category_dict, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = SubCategorySerializer(sub_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        sub_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def FetchSubCategoriesView(request, shop, id):
    try:
        sub_category = SubCategory.objects.get(shop_id=shop, id=id)
    except SubCategory.DoesNotExist:
        return Response(
            {"error": "SubCategory with the given ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    # Fetch related SubCategoryAttributes and their associated Attributes and Variations
    sub_category_attributes = SubCategoryAttribute.objects.filter(sub_category_id=sub_category.id).select_related('attribute')
    response_data = []
    for sub_cat_attr in sub_category_attributes:
        attribute = sub_cat_attr.attribute
        if not attribute:
            continue
        variations = Variation.objects.filter(shop_id=shop, attribute_name_id=attribute.id).values_list('variation_name', flat=True)
        response_data.append({
            "id": sub_category.id,
            "sub_category": sub_category.sub_category_name,
            "attribute": attribute.attribute_name,
            "variation": list(variations),
        })
    return Response(response_data, status=status.HTTP_200_OK)


### FETCH ALL CATEGORIES ACCORDING TO THEIR SUB_CATEGORIES VIEW
@api_view(["GET"])
def FetchParentCategoryView(request, shop, code):
    p_category = ParentCategory.objects.filter(shop_id=shop, hc_name_id=code)
    serializer = ParentCategorySerializer(p_category, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def FetchCategoryView(request, shop, code):
    category = Category.objects.filter(shop_id=shop, pc_name_id=code)
    category_array = []
    if len(category) > 0:
        for i in range(len(category)):
            category_dict = dict()
            category_dict["id"] = category[i].id
            category_dict["category_name"] = category[i].category_name
            category_dict["symbol"] = category[i].symbol
            category_dict["description"] = category[i].description
            category_dict["status"] = category[i].status
            category_dict["pc_name"] = category[i].pc_name_id
            category_dict["shop"] = category[i].shop_id
            category_array.append(category_dict)
    return Response(category_array)


@api_view(["GET"])
def FetchSubCategoryView(request, shop, code):
    sub_category = SubCategory.objects.filter(shop_id=shop, category_id=code)
    sub_category_array = []
    if len(sub_category) > 0:
        for i in range(len(sub_category)):
            sub_category_dict = dict()
            sub_category_dict["id"] = sub_category[i].id
            sub_category_dict["sub_category_name"] = sub_category[i].sub_category_name
            sub_category_dict["symbol"] = sub_category[i].symbol
            sub_category_dict["description"] = sub_category[i].description
            sub_category_dict["status"] = sub_category[i].status
            sub_category_dict["category"] = sub_category[i].category_id
            sub_category_dict["shop"] = sub_category[i].shop_id
            sub_category_array.append(sub_category_dict)
    return Response(sub_category_array)


### TEMPORARY PRODUCT VIEW
class AddTemporaryProductView(generics.ListCreateAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = TempProductSerializer
    pagination_class = None
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = TemporaryProduct.objects.filter(shop_id=get_shop).order_by("id")
        return queryset

class TemporaryProductGetView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TempProductSerializer
    pagination_class = None
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = TemporaryProduct.objects.filter(shop_id=get_shop).order_by("id")
        return queryset
    
@api_view(["DELETE"])
def DeleteTemporaryProductView(request, shop):
    try:
        # Delete all rows
        TemporaryProduct.objects.filter(shop_id=shop).delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### PRODUCT VIEW
class AddProduct(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = Product.objects.filter(shop_id=get_shop).order_by("id")
        return queryset
    

class ProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = None
    
    def get_queryset(self):
        get_shop = self.kwargs.get('shop')
        queryset = Product.objects.filter(shop_id=get_shop).order_by("id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_stock = Stock.objects.filter(
            product_name=instance.product_name, sku=instance.sku
        )
        delete_stock.delete()
        self.perform_destroy(instance)
        return Response(status="200")
    
    
@api_view(['GET'])    
def ShowAllProductView(request,shop, outlet):
    try:
        get_outlet = Outlet.objects.get(shop_id=shop, id=outlet)
    except Outlet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    products = Product.objects.filter(shop_id=shop, outlet_id=outlet).distinct('product_name').select_related('outlet', 'brand')
    serializer = ShowAllProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET']) 
def ShowAllProductDetailView(request, shop, product_id):
    try:
        ### Retrieve the product and its name
        get_product_name = Product.objects.get(shop_id=shop, id=product_id).product_name
    except Product.DoesNotExist:
        raise NotFound(detail=f"Product with ID {product_id} does not exist.")
    ### FILTER PRODUCTS DETAIL
    products = Product.objects.filter(shop_id=shop, product_name=get_product_name).select_related('outlet', 'brand', 'category__pc_name__hc_name', 'sub_category')

    product_header_array = []
    product_detail_array = []

    product_dict = dict()

    if products.exists:
            product = products[0]  ### Fetch the first product
            product_dict = {
             
                "product_name": product.product_name,
                "outlet": product.outlet.outlet_name if product.outlet else None,
                "head_category": getattr(product.category.pc_name.hc_name, 'hc_name', None) if product.category else None,
                "parent_category": getattr(product.category.pc_name, 'pc_name', None) if product.category else None,
                "category": getattr(product.category, 'category_name', None) if product.category else None,
                "sub_category": getattr(product.sub_category, 'sub_category_name', None),
            }
            product_header_array.append(product_dict)
    ### OTHER DETAIL
    for product in products:
        product_detail_array.append({
            'id': product.id,
            "description": product.description,
            "color": product.color,
            "sku": product.sku,
            "cost_price": product.cost_price,
            "selling_price": product.selling_price,
            "discount_price": product.discount_price,
            "wholesale_price": product.wholesale_price,
            "retail_price": product.retail_price,
            "token_price": product.token_price
        })
        
    param = {
            "header_array": product_header_array,
            "detail_array": product_detail_array,
        }
    return Response(param)


@api_view(['GET']) 
def BarcodeDataView(request,shop, sku):
    try:
        get_product = Product.objects.get(shop_id=shop, sku=sku)
    except Outlet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(get_product)
    return Response(serializer.data)
   


### FETCH ALL PRODUCT NAME WITH OUTLET CODE AND STOCK VIEW
@api_view(["GET"])
def GetAllProductView(request, shop, outlet_id):
    cursor = connections["default"].cursor()
    query_employee = "select distinct outlet_code ||'--' ||product_name as product_name, product_name as product_code  from tbl_product pr INNER JOIN tbl_outlet ot on pr.outlet_id = ot.id where ot.id = '"+ outlet_id +"' and pr.shop_id = '"+ shop +"' ORDER BY product_name"
    cursor.execute(query_employee)
    product_name = DistinctFetchAll(cursor)
    return Response(product_name)





### FETCH ALL VARIATION ACCORDING TO ATTRIBUTE AND ITS TYPES VIEW
# @api_view(["GET"])
# def FetchAllAttributeTypeView(request):
#     cursor = connections["default"].cursor()
#     query = "SELECT att_type from tbl_attribute_type"
#     cursor.execute(query)
#     all_attribute_type = DistinctFetchAll(cursor)
#     return Response(all_attribute_type)


# @api_view(["GET"])
# def FetchAttributeView(request, code):
#     cursor = connections["default"].cursor()
#     query = (
#         "select attribute_name from tbl_attribute where att_type_id = '" + code + "'"
#     )
#     cursor.execute(query)
#     fetch_attribute = DistinctFetchAll(cursor)
#     return Response(fetch_attribute)


# @api_view(["GET"])
# def FetchVariationView(request, code):
#     cursor = connections["default"].cursor()
#     query_employee = (
#         "SELECT variation_name, symbol FROM tbl_variation where attribute_name_id = '"
#         + code
#         + "'"
#     )
#     cursor.execute(query_employee)
#     employee_location = DistinctFetchAll(cursor)
#     return Response(employee_location)

