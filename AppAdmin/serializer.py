from rest_framework import serializers
from .models import ShopOwner


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = '__all__'