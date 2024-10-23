from django.shortcuts import render

# Create your views here.
from rest_framework.generics import *
from .models import *
from .serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse


# class AddStockView(RetrieveUpdateAPIView):
#     queryset = Stock.objects.all()
#     # serializer_class = StockSerializer(queryset, many=True)
#     serializer_class = StockSerializer


@api_view(['GET', 'PUT'])
def AddStockView(request, code):
    stock = Stock.objects.filter(product_name=code).order_by('id')
    if request.method == 'GET':

        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        list_serializer = []
        for x in range(len(stock)):
            serializer = StockSerializer(stock[x], data=request.data[x])
            if serializer.is_valid():
                serializer.save()
                list_serializer.append(serializer)
        return Response('Stock Updated')
