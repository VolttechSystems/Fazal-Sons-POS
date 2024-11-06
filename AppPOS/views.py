from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import generics


# Create your views here.

class AddTransactionView(generics.ListCreateAPIView):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    pagination_class = None
    

class AddAdditionalFeeView(generics.ListCreateAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None
    
class GetAdditionalFeeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdditionalFee.objects.all()
    serializer_class = AdditionalFeeSerializer
    pagination_class = None


