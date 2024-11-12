from .models import *
from .serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status





@api_view(['PUT'])
def AddStockView(request):
    if not isinstance(request.data, list):  # Ensure the request data is a list
        return Response({'detail': 'Expected a list of items.'}, status=status.HTTP_400_BAD_REQUEST)

    updated_stock= []
    errors = []

    for item in request.data:
        try:
            stock = Stock.objects.get(sku=item['sku'])
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


# class AddStockView(generics.RetrieveUpdateAPIView):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer
#     pagination_class = None


# [
#     {
#         "avail_quantity": "12",
#         "sku": "PR-13"
#     },
#     {
#         "avail_quantity": "0",
#         "sku": "PR-14"
#     }
# ]
