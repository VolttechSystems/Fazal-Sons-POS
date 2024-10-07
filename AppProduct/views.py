from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from django.http import Http404
from django.http import JsonResponse, HttpResponse

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# FUNCTION THAT CREATE TOKEN WHEN USER IS CREATED
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CreateUserView(generics.ListCreateAPIView):
    model = get_user_model()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddBrandView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@api_view(['GET', 'POST'])
def AddAttributeView(request):
    if request.method == "GET":
        attribute = Attribute.objects.all()
        if len(attribute) > 0:
            serializer = AttributeSerializer(attribute, many=True)
            param = {
                'status': 200,
                'data': serializer.data,
            }
            return Response(param)
        raise Http404
    elif request.method == 'POST':
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def AttributeGetView(request, id):
    attribute = Attribute.objects.get(id=id)

    if request.method == "GET":
        attribute_serializer = AttributeSerializer(attribute)
        return Response(attribute_serializer.data)
    elif request.method == "DELETE":
        attribute.delete()
        return Response("Deleted")
    elif request.method == "PUT":
        attribute_serializer = AttributeSerializer(attribute, data=request.data)
        if attribute_serializer.is_valid():
            attribute_serializer.save()
            return Response(attribute_serializer.data, status=200)
    return Response("Error! Nothing Happened")


@api_view(['GET', 'POST'])
def AddVariationView(request):
    if request.method == "GET":
        variation = Variation.objects.all()
        if len(variation) > 0:
            serializer = VariationSerializer(variation, many=True)
            param = {
                'status': 200,
                'data': serializer.data,
            }
            return Response(param)
        raise Http404
    elif request.method == 'POST':
        serializer = VariationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def VariationGetView(request, id):
    variation = Variation.objects.get(id=id)
    if request.method == "GET":
        variation_serialzer = VariationSerializer(variation)
        return Response(variation_serialzer.data)
    elif request.method == "DELETE":
        variation.delete()
        return Response("Deleted")
    elif request.method == "PUT":
        variation_serialzer = VariationSerializer(variation, data=request.data)
        if variation_serialzer.is_valid():
            variation_serialzer.save()
            return Response(variation_serialzer.data, status=200)
    return Response("Error! Nothing Happened")


@api_view(['GET', 'POST'])
def AddParentCategoryView(request):
    if request.method == "GET":
        parent_category = ParentCategory.objects.all()
        if len(parent_category) > 0:
            pc_serializer = ParentCategorySerializer(parent_category, many=True)
            param = {
                'status': 200,
                'data': pc_serializer.data,
            }
            return Response(param)
        raise Http404
    elif request.method == "POST":
        pc_serializer = ParentCategorySerializer(data=request.data)
        if pc_serializer.is_valid():
            pc_serializer.save()
            return Response(pc_serializer.data)
        return Response(pc_serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def ParentCategoryGetView(request, id):
    p_category = ParentCategory.objects.get(id=id)

    if request.method == 'GET':
        pc_serializer = ParentCategorySerializer(p_category)
        return Response(pc_serializer.data)
    elif request.method == 'DELETE':
        p_category.delete()
        return Response("Deleted")
    elif request.method == 'PUT':
        pc_serializer = ParentCategorySerializer(p_category, data=request.data)
        if pc_serializer.is_valid():
            pc_serializer.save()
            return Response(pc_serializer.data)
    return Response("Error! Nothing Happened")


@api_view(['GET', 'POST'])
def AddCategoryView(request):
    if request.method == "GET":
        category = Category.objects.all()
        if len(category) > 0:
            category_serializer = CategorySerializer(category, many=True)
            param = {
                'status': 200,
                'data': category_serializer.data,
            }
            return Response(param)
        raise Http404
    elif request.method == "POST":
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data)
        return Response(category_serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def CategoryGetView(request, id):
    category = Category.objects.get(id=id)

    if request.method == 'GET':
        category_serializer = CategorySerializer(category)
        return Response(category_serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response("Deleted")
    elif request.method == 'PUT':
        category_serializer = CategorySerializer(category, data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data)
    return Response("Error! Nothing Happened")


class AddSubCategoryView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class AddProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
