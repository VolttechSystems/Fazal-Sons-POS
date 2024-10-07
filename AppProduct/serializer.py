from rest_framework import serializers
from AppProduct.models import *
import datetime
from django.contrib.auth import get_user_model

UserModel = get_user_model()


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


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        brand = super().create(validated_data)
        brand.updated_at = None
        brand.save()
        return brand

    def update(self, instance, validated_data):
        brand = super().update(instance, validated_data)
        brand.updated_at = datetime.datetime.now()
        brand.save()
        return brand


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

    def create(self, validated_data):
        attribute = super().create(validated_data)
        attribute.updated_at = None
        attribute.save()
        return attribute

    def update(self, instance, validated_data):
        attribute = super().update(instance, validated_data)
        attribute.updated_at = datetime.datetime.now()
        attribute.save()
        return attribute


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = "__all__"

    def create(self, validated_data):
        p_category = super().create(validated_data)
        p_category.created_at = datetime.datetime.now()
        p_category.updated_at = None
        p_category.save()
        return p_category

    def update(self, instance, validated_data):
        p_category = super().update(instance, validated_data)
        p_category.updated_at = datetime.datetime.now()
        p_category.save()
        return p_category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, data):
        category = super().create(data)
        category.created_at = datetime.datetime.now()
        category.updated_at = None
        category.save()
        return category

    def update(self, instance, data):
        category = super().update(instance, data)
        category.updated_at = datetime.datetime.now()
        category.save()
        return category


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

    def create(self, validated_data):
        sub_category = super().create(validated_data)
        sub_category.created_at = datetime.datetime.now()
        sub_category.updated_at = None
        sub_category.save()
        return sub_category

    def update(self, instance, validated_data):
        sub_category = super().update(instance, validated_data)
        sub_category.updated_at = datetime.datetime.now()
        sub_category.save()
        return sub_category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
