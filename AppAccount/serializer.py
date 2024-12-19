from rest_framework import serializers
import datetime
from django.contrib.auth import get_user_model
from .models import *
UserModel = get_user_model()
DateTime = datetime.datetime.now()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    system_roles = serializers.PrimaryKeyRelatedField(
        queryset=SystemRole.objects.all(), 
        many=True, 
        required=False  # Make it optional for creation
    )
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'password', 'system_roles']


    def create(self, validated_data):
        system_roles_data = validated_data.pop('system_roles', [])
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
        )
        # Assign system roles to the UserProfile
        if system_roles_data:
            user_profile = UserProfile.objects.create(user=user)
            user_profile.system_roles.set(system_roles_data)  # Set the many-to-many relationships

        return user

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class SystemRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRole
        fields = "__all__"
    
