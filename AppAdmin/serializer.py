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
    # system_roles = serializers.PrimaryKeyRelatedField(
    #     queryset=SystemRole.objects.all(), 
    #     many=True, 
    #     required=False  # Make it optional for creation
    # )
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), 
        required=False  # Make it optional for creation
    )
    class Meta:
        model = UserModel
        fields = ['id','username', 'first_name', 'last_name', 'email', 'is_active', 'password', 'phone_number', 'shop' ]


    def create(self, validated_data):
        get_shop = validated_data.pop('shop', None)
        print(get_shop)
        phone_number = validated_data.pop('phone_number', None)
        
        # if shop:
        #     existing_profile = UserProfile.objects.filter(shop=shop, user__username=validated_data['username']).first()
        #     if existing_profile:
        #         raise serializers.ValidationError({
        #             'username': f"A user with username '{validated_data['username']}' already exists for this shop."
        #         })
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