from rest_framework.serializers import *
from .models import *

### UPDATE STOCK SERIALIZER 
class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'product_name', 'avail_quantity', 'sku', 'color', 'size')
        
    def update(self, instance, validated_data):
        stock = validated_data
        print(stock)
        stock_quantity = int(validated_data.get('avail_quantity'))
        stock = int(Stock.objects.get(sku=instance).avail_quantity)
        stock += stock_quantity
        validated_data['avail_quantity'] = stock
        stock = super().update(instance, validated_data)
        return stock


    # def update(self, instance, validated_data):
    #     sku = validated_data.get('sku')
    #     avail_quantity = validated_data.get('avail_quantity')
    #     print(sku)
    #     print(avail_quantity)
    #     # stock_quantity = int(validated_data.get('avail_quantity'))
    #     # stock = int(Stock.objects.get(sku=instance).avail_quantity)
    #     # stock += stock_quantity
    #     # validated_data['avail_quantity'] = stock
    #     # stock = super().update(instance, validated_data)
    #     return sku
    
    # def create(self, validated_data):
    #     parent = ''
    #     sku = validated_data.get('sku')
    #     print(sku)


    # def update(self, instance, validated_data):

        # instance.content = validated_data.get('content', instance.content)
        # stock = super().update(instance, validated_data)
        # stock.save()