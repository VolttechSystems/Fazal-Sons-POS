from rest_framework.serializers import *
from .models import *

### UPDATE STOCK SERIALIZER 
class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'product_name', 'avail_quantity', 'sku', 'color')
        
    def update(self, instance, validated_data):
        stock = validated_data
        print(stock)
        stock_quantity = int(validated_data.get('avail_quantity'))
        stock = int(Stock.objects.get(sku=instance).avail_quantity)
        stock += stock_quantity
        validated_data['avail_quantity'] = stock
        stock = super().update(instance, validated_data)
        return stock