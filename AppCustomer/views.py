from django.shortcuts import render
from .serializer import *
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class AddCustomerChannel(ListCreateAPIView):
    queryset = CustomerChannel.objects.all()
    serializer_class = CustomerChannelSerializer
    pagination_class = None


class GetCustomerChannel(RetrieveUpdateDestroyAPIView):
    queryset = CustomerChannel.objects.all()
    serializer_class = CustomerChannelSerializer
    pagination_class = None


class AddCustomerType(ListCreateAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    pagination_class = None


class GetCustomerType(RetrieveUpdateDestroyAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    pagination_class = None


class AddCustomer(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = None


class GetCustomer(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = None
