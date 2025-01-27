from .models import *
from .serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import generics
from rest_framework import status


@api_view(['PUT', 'GET'])
def AddStockView(request, shop, code):
    if request.method == 'GET':
        stock = Stock.objects.filter(shop_id=shop, product_name=code)
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not isinstance(request.data, list):  # Ensure the request data is a list
            return Response({'detail': 'Expected a list of items.'}, status=status.HTTP_400_BAD_REQUEST)
        updated_stock = []
        errors = []
        for item in request.data:
            try:
                stock = Stock.objects.get(shop_id=shop, sku=item['sku'])
                serializer = StockSerializer(stock, data=item, partial=True)  # partial=True allows partial updates
                if serializer.is_valid():
                    serializer.save()
                    updated_stock.append(serializer.data)
                else:
                    errors.append({item['sku']: serializer.errors})
            except Stock.DoesNotExist:
                errors.append({item['sku']: 'Stock with this sku not found.'})
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'updated_stock': updated_stock}, status=status.HTTP_200_OK)
