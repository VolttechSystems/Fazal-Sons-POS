from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import generics


### TRANSACTION VIEW
class AddTransactionView(generics.ListCreateAPIView):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    pagination_class = None
    
### ADDITIONAL FEE VIEW
class AddAdditionalFeeView(generics.ListCreateAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None
    
class GetAdditionalFeeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None

    
### SALESMAN VIEW
class AddSalesmanView(generics.ListCreateAPIView):
    queryset = Salesman.objects.all()
    serializer_class = AddSalesmanSerializer
    pagination_class = None
    
class GetSalesmanView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salesman.objects.all()
    serializer_class = AddSalesmanSerializer
    pagination_class = None
    

            
    





