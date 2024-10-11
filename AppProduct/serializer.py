from rest_framework import serializers
from AppProduct.models import *
import datetime

DateTime = datetime.datetime.now()



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        brand = super().create(validated_data)
        brand.updated_at = None
        brand.created_at = DateTime
        brand.save()
        return brand

    def update(self, instance, validated_data):
        brand = super().update(instance, validated_data)
        brand.updated_at = DateTime
        brand.save()
        return brand


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

    def create(self, validated_data):
        attribute = super().create(validated_data)
        attribute.updated_at = None
        attribute.created_at = DateTime
        attribute.save()
        return attribute

    def update(self, instance, validated_data):
        attribute = super().update(instance, validated_data)
        attribute.updated_at = DateTime
        attribute.save()
        return attribute


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'

    def create(self, validated_data):
        variation = super().create(validated_data)
        variation.updated_at = None
        variation.created_at = DateTime
        variation.save()
        return variation

    def update(self, instance, validated_data):
        variation = super().update(instance, validated_data)
        variation.updated_at = DateTime
        variation.save()
        return variation


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = "__all__"

    def create(self, validated_data):
        p_category = super().create(validated_data)
        p_category.created_at = DateTime
        p_category.updated_at = None
        p_category.save()
        return p_category

    def update(self, instance, validated_data):
        p_category = super().update(instance, validated_data)
        p_category.updated_at = DateTime
        p_category.save()
        return p_category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, data):
        category = super().create(data)
        category.created_at = DateTime
        category.updated_at = None
        category.save()
        return category

    def update(self, instance, data):
        category = super().update(instance, data)
        category.updated_at = DateTime
        category.save()
        return category


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

    def create(self, validated_data):
        sub_category = super().create(validated_data)
        sub_category.created_at = DateTime
        sub_category.updated_at = None
        sub_category.save()
        return sub_category

    def update(self, instance, validated_data):
        sub_category = super().update(instance, validated_data)
        sub_category.updated_at = DateTime
        sub_category.save()
        return sub_category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
