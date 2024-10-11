from rest_framework import serializers
import datetime
from django.contrib.auth import get_user_model

UserModel = get_user_model()
DateTime = datetime.datetime.now()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "first_name", "last_name", "email", "is_staff", "is_active")


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
