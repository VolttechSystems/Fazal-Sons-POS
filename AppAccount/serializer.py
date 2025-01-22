from rest_framework import serializers
import datetime
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
UserModel = get_user_model()
DateTime = datetime.datetime.now()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    shop = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    system_roles = serializers.PrimaryKeyRelatedField(
        queryset=SystemRole.objects.all(), 
        many=True, 
        required=False  # Make it optional for creation
    )
    outlet = serializers.PrimaryKeyRelatedField(
        queryset=Outlet.objects.all(), 
        many=True, 
        required=False  # Make it optional for creation
    )
    class Meta:
        model = UserModel
        fields = ['id','username', 'first_name', 'last_name', 'email', 'is_active', 'password', 'phone_number', 'system_roles', 'outlet', 'shop']


    def create(self, validated_data):
        system_roles_data = validated_data.pop('system_roles', [])
        outlet_data = validated_data.pop('outlet', [])
        phone_number = validated_data.pop('phone_number', None)
        shop = validated_data.pop('shop', None)
        print(shop)
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
        )
        
        user_profile = UserProfile.objects.create(user=user,  phone_number=phone_number, shop_id=shop)
        # Assign system roles to the UserProfile
        if system_roles_data:
            user_profile.system_roles.set(system_roles_data)  # Set the many-to-many relationships
        if outlet_data:
            user_profile.outlet.set(outlet_data)  # Set outlets to the users

        return user

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermissions
        fields = ['id','permission_name']
    
class SystemRoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = SystemRole
        fields = "__all__"

class PostSystemRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRole
        fields = "__all__"
    def create(self, validated_data):
        validated_data['created_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                    validated_data['created_by'] = request.user.username
        system_role = super().create(validated_data)
        return system_role
    
    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user.username
        salesman = super().update(instance, validated_data)
        return validated_data
    
class FetchSystemRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRole
        fields = ['id', 'sys_role_name']

    
class AdminChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value
    

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    is_active = serializers.BooleanField(source='user.is_active')
    shop = serializers.CharField(source='shop.id', read_only=True)
    system_roles = serializers.SerializerMethodField()
    outlet = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'phone_number', 'is_active', 'system_roles', 'outlet' ,'shop']

    def get_system_roles(self, obj):
        return obj.system_roles.values('id', 'sys_role_name')

    def get_outlet(self, obj):
        return obj.outlet.values('id', 'outlet_name')