from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from AppProduct.models import Outlet
from AppAdmin.models import Shop
from AppAccount.models import SystemRole
UserModel = get_user_model()
from AppAccount.models import UserProfile


class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        
        

class ShopAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), 
        required=False 
    )
    class Meta:
        model = UserModel
        fields = ['id','username', 'first_name', 'last_name', 'email', 'is_active', 'password', 'phone_number', 'shop' ]


    def create(self, validated_data):
        get_shop = validated_data.pop('shop', None)
        phone_number = validated_data.pop('phone_number', None)
        
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_staff=True,
            is_active=validated_data['is_active'],
        )
        
        user_profile = UserProfile.objects.create(user=user,  phone_number=phone_number, shop=get_shop)

        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    is_staff = serializers.BooleanField(source='user.is_staff')
    is_active = serializers.BooleanField(source='user.is_active')
    shop = serializers.CharField(source='shop.name', read_only=True)
   


    class Meta:
        model = UserProfile 
        fields = ['id', 'username', 'email', 'phone_number', 'is_staff',  'is_active','shop']