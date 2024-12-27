from .models import *
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
from rest_framework.permissions import IsAuthenticated



@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated,IsStock])
def AddStockView(request, product_name):
    if request.method == 'GET':
        stock = Stock.objects.filter(product_name=product_name)
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not isinstance(request.data, list):  # Ensure the request data is a list
            return Response({'detail': 'Expected a list of items.'}, status=status.HTTP_400_BAD_REQUEST)
        updated_stock = []
        errors = []
        for item in request.data:
            try:
                stock = Stock.objects.get(sku=item['sku'])
                serializer = StockSerializer(stock, data=item, partial=True ,  context={'request': request})  # partial=True allows partial updates
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
