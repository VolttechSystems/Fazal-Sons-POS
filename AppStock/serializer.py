from rest_framework.serializers import *
from .models import *


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    # def get_serializer(self, *args, **kwargs):
    #     ProductView = ''
    #     if isinstance(kwargs.get("data", {}), list):
    #         kwargs["many"] = True
    #     return super(ProductView, self).get_serializer(*args, **kwargs)

    # def update(self, instance, validated_data):
    #     # stock = Stock.objects.filter(product_name=code).order_by('id')
    #     stock = validated_data
    #     stock_quantity = int(validated_data.get('avail_quantity'))
    #     stock = int(Stock.objects.get(sku=instance).avail_quantity)
    #     stock += stock_quantity
    #     validated_data['avail_quantity'] = stock
    #     stock = super().update(instance, validated_data)
    #     return stock
