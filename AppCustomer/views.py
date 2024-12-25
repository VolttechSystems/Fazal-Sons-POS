from .serializer import *
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .permissions import * 
from AppProduct.views import MyLimitOffsetPagination


# Create your views here.

### CUSTOMER CHANNEL VIEW
class AddCustomerChannel(ListCreateAPIView):
    queryset = CustomerChannel.objects.all()
    serializer_class = CustomerChannelSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    pagination_class = MyLimitOffsetPagination

class GetCustomerChannel(RetrieveUpdateDestroyAPIView):
    queryset = CustomerChannel.objects.all()
    serializer_class = CustomerChannelSerializer
    permission_classes = [IsAuthenticated, IsCustomer]


### CUSTOMER TYPE VIEW
class AddCustomerType(ListCreateAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    pagination_class = MyLimitOffsetPagination


class GetCustomerType(RetrieveUpdateDestroyAPIView):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

### CUSTOMER VIEW
class AddCustomer(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsCustomer]  
    pagination_class = MyLimitOffsetPagination


class GetCustomer(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsCustomer] 
