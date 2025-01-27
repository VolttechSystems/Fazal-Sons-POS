from django.shortcuts import render
from .serializer import *
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from AppProduct.views import LimitOffsetPagination


### CUSTOMER CHANNEL VIEW
class AddCustomerChannel(ListCreateAPIView):
    serializer_class = CustomerChannelSerializer
    pagination_class = None
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        queryset = CustomerChannel.objects.filter(shop_id=shop_id)
        return queryset
        
class GetCustomerChannel(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerChannelSerializer
    pagination_class = None
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        queryset = CustomerChannel.objects.filter(shop_id=shop_id)
        return queryset


### CUSTOMER TYPE VIEW
class AddCustomerType(ListCreateAPIView):
    serializer_class = CustomerTypeSerializer
    pagination_class = None
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        queryset = CustomerType.objects.filter(shop_id=shop_id)
        return queryset

class GetCustomerType(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerTypeSerializer
    pagination_class = None
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        queryset = CustomerType.objects.filter(shop_id=shop_id)
        return queryset

### CUSTOMER VIEW
class AddCustomer(ListCreateAPIView):
    serializer_class = CustomerSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        outlet_id = self.kwargs.get('outlet')
        queryset = Customer.objects.filter(shop_id=shop_id, outlet_id=outlet_id)
        return queryset
    

class GetCustomer(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    pagination_class = None
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop')
        outlet_id = self.kwargs.get('outlet')
        queryset = Customer.objects.filter(shop_id=shop_id, outlet_id=outlet_id)
        return queryset
