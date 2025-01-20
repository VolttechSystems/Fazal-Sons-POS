from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.permissions import IsAdminUser


class AddShopView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ShopOwner.objects.all() 
    serializer_class = ShopOwnerSerializer