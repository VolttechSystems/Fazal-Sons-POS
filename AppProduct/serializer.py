from rest_framework import serializers
from AppProduct.models import *
import datetime

DateTime = datetime.datetime.now()


# BRAND
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


# ATTRIBUTE TYPE
class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeType
        fields = '__all__'

    def create(self, validated_data):
        attr_type = super().create(validated_data)
        attr_type.updated_at = None
        attr_type.created_at = DateTime
        attr_type.save()
        return attr_type

    def update(self, instance, validated_data):
        attr_type = super().update(instance, validated_data)
        attr_type.updated_at = DateTime
        attr_type.save()
        return attr_type


# ATTRIBUTE
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


# VARIATION
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


# HEAD CATEGORY
class HeadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadCategory
        fields = "__all__"

    def create(self, validated_data):
        h_category = super().create(validated_data)
        h_category.created_at = DateTime
        h_category.updated_at = None
        h_category.save()
        return h_category

    def update(self, instance, validated_data):
        h_category = super().update(instance, validated_data)
        h_category.updated_at = DateTime
        h_category.save()
        return h_category


# PARENT CATEGORY
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


# CATEGORY
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


# SUB CATEGORY
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


# PRODUCT
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):

        # parent = ''
        # used_for_inventory = validated_data.get('used_for_inventory')
        # colors = validated_data.get('color')
        # sizes = validated_data.get('size')
        # split_color = colors.split("^")
        # len_color = len(split_color)
        #
        # split_size = sizes.split("^")
        # len_size = len(split_size)
        #
        # if used_for_inventory == 'true':
        #     if len_color > 0:
        #         for size in range(len_size):
        #             for color in range(len_color):
        #                 validated_data['size'] = split_size[size]
        #                 validated_data['color'] = split_color[color]
        #                 parent = super().create(validated_data)
        # else:
        #     if len_size > 0:
        #         for size in range(len_size):
        #             validated_data['size'] = split_size[size]
        #             parent = super().create(validated_data)
        # return parent

        parent = ''
        used_for_inventory = validated_data.get('used_for_inventory')
        colors = validated_data.get('color')
        colors = colors.replace("'", "")
        colors = colors.replace("[", "")
        colors = colors.replace("]", "")

        sizes = validated_data.get('size')
        sizes = sizes.replace("'", "")
        sizes = sizes.replace("[", "")
        sizes = sizes.replace("]", "")

        split_color = colors.split(",")
        len_color = len(split_color)

        split_size = sizes.split(",")
        len_size = len(split_size)

        if used_for_inventory == 'true':
            if len_color > 0:
                for size in range(len_size):
                    for color in range(len_color):
                        validated_data['size'] = split_size[size].strip()
                        validated_data['color'] = split_color[color].strip()
                        parent = super().create(validated_data)
        else:
            if len_size > 0:
                for size in range(len_size):
                    validated_data['size'] = split_size[size].strip()
                    validated_data['color'] = 'None'
                    parent = super().create(validated_data)
        return parent
