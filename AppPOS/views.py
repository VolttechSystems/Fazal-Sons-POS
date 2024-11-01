from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import generics


# Create your views here.

class AddTransactionView(generics.ListCreateAPIView):
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer
    pagination_class = None
