from rest_framework import serializers
from AppProduct.models import *
import datetime
from AppCustomer.utils import *
from AppStock.models import *
from rest_framework import status
from rest_framework.response import Response

DateTime = datetime.datetime.now()


### OUTLET SERIALIZER
class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ['outlet_code', 'outlet_name']

    def create(self, validated_data):
        outlet = super().create(validated_data)
        outlet.updated_at = None
        outlet.created_at = DateTime
        outlet.save()
        return outlet

    def update(self, instance, validated_data):
        outlet = super().update(instance, validated_data)
        outlet.updated_at = DateTime
        outlet.save()
        return outlet


### BRAND SERIALIZER
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


### ATTRIBUTE TYPE SERIALIZER
class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeType
        fields = ['id', 'att_type', 'status']

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


### ATTRIBUTE SERIALIZER
class AttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Attribute
        fields = ['id', 'attribute_name', 'symbol', 'description', 'status', 'att_type']

    def create(self, validated_data):
        attribute_names = validated_data.get('attribute_name')
        # print(attribute_name)
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


### VARIATION SERIALIZER
class VariationSerializer(serializers.ModelSerializer):
    # attribute_name = AttributeSerializer('id')
    class Meta:
        model = Variation
        # fields = ['id','variation_name','symbol', 'description', 'status', 'attribute_name']
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


### HEAD CATEGORY SERIALIZER
class HeadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadCategory
        fields = ['hc_name', 'symbol', 'description', 'status']

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


### PARENT CATEGORY SERIALIZER
class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = ['id','pc_name', 'symbol', 'description', 'status', 'hc_name']

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


### CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    attribute_group = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        get_subcategory_option = validated_data.get('subcategory_option')
        if get_subcategory_option == 'True':
            validated_data['attribute_group'] = []
        validated_data['created_at'] = DateTime
        validated_data['updated_at'] = None
        category = super().create(validated_data)
        return category

    def update(self, instance, validated_data):
        get_subcategory_option = validated_data.get('subcategory_option')
        if get_subcategory_option == 'True':
            validated_data['attribute_group'] = []
        validated_data['updated_at'] = DateTime
        category = super().update(instance, validated_data)
        return category


### SUB CATEGORY SERIALIZER
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


class VariationSerializers(serializers.Serializer):
    color = serializers.CharField(max_length=100)
    size = serializers.CharField(max_length=100)


### TEMPORARY PRODUCT SERIALIZER
class TempProductSerializer(serializers.ModelSerializer):
    color = serializers.ListField(child=serializers.CharField())
    attribute = serializers.ListField(child=serializers.CharField())
    variations = serializers.ListField(child=serializers.ListField())

    # variations = serializers.CharField(max_length=255)
    # variations = VariationSerializers(many=True)

    class Meta:
        model = TemporaryProduct
        fields = '__all__'

    def validate_size(self, value):
        if value == None:
            raise serializers.ValidationError("Please Select Sizes")
        return value

    def create(self, validated_data):
        parent = ''
        get_color = validated_data.get('color')
        get_attribute = validated_data.get('attribute')
        get_variations = validated_data.get('variations')
        len_variation = len(get_variations)
        if len(get_variations) > 0:
            Dict = dict()

            vriation_array = []
            for i in range(0, 1):
                var = get_variations[0]
                for y in range(len(var)):
                    bb = var[y]
                    for x in range(1, len_variation):
                        vars = get_variations[x]
                        for z in range(len(vars)):
                            aa = vars[z]

                            final = str(bb) + "-" + str(aa)
                            vriation_array.append(final)


            # len_var = len(var)
            # if len_var > 0:
            #     for x in range(len_variation):
            #         g = var[x]

        # for color in range(len(get_color)):
        #     # for attribute in range(len(get_attribute)):
        #     for variation in range(len(get_variations)):
        #         auto_sku_code = AutoGenerateCodeForModel(TemporaryProduct, 'sku', 'PR-')
        #         validated_data['sku'] = auto_sku_code
        #         validated_data['color'] = get_color[color]
        #         validated_data['size'] = get_variations[variation]
        #         validated_data['created_at'] = DateTime
        # parent = super().create(validated_data)
        return parent


# sizes = validated_data.get('size')
# sizes = sizes.replace("'", "")
# sizes = sizes.replace("[", "")
# sizes = sizes.replace("]", "")
#
# split_color = colors.split(",")
# len_color = len(split_color)
#
# split_size = sizes.split(",")
# len_size = len(split_size)
#
# if used_for_inventory == 'true':
#     if len_color > 0:
#         for size in range(len_size):
#             for color in range(len_color):
#                 auto_sku_code = AutoGenerateCodeForModel(TemporaryProduct, 'sku', 'PR-')
#                 validated_data['sku'] = auto_sku_code
#                 validated_data['size'] = split_size[size].strip()
#                 validated_data['color'] = split_color[color].strip()
#                 validated_data['created_at'] = DateTime
#                 parent = super().create(validated_data)
# else:
#     if len_size > 0:
#         for size in range(len_size):
#             auto_sku_code = AutoGenerateCodeForModel(TemporaryProduct, 'sku', 'PR-')
#             validated_data['sku'] = auto_sku_code
#             validated_data['size'] = split_size[size].strip()
#             validated_data['color'] = 'None'
#             validated_data['created_at'] = DateTime
#             parent = super().create(validated_data)


def update(self, instance, validated_data):
    validated_data['updated_at'] = DateTime
    parent = super().update(instance, validated_data)
    return parent


### PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        parent = ''
        tem_product = TemporaryProduct.objects.all()
        len_tem_product = len(tem_product)
        for x in range(len_tem_product):
            auto_code = AutoGenerateCodeForModel(Product, 'sku', 'PR-')
            validated_data['product_name'] = tem_product[x].product_name
            validated_data['sku'] = auto_code
            validated_data['outlet_name'] = tem_product[x].outlet_name
            validated_data['sub_category_name'] = tem_product[x].sub_category_name
            validated_data['brand_name'] = tem_product[x].brand_name
            validated_data['season'] = tem_product[x].season
            validated_data['description'] = tem_product[x].description
            validated_data['color'] = tem_product[x].color
            validated_data['size'] = tem_product[x].size
            validated_data['image'] = tem_product[x].image
            validated_data['used_for_inventory'] = tem_product[x].used_for_inventory
            validated_data['cost_price'] = tem_product[x].cost_price
            validated_data['selling_price'] = tem_product[x].selling_price
            validated_data['discount_price'] = tem_product[x].discount_price
            validated_data['wholesale_price'] = tem_product[x].wholesale_price
            validated_data['retail_price'] = tem_product[x].retail_price
            validated_data['token_price'] = tem_product[x].token_price
            validated_data['created_at'] = DateTime
            # Add Stock
            add_stock = Stock(
                product_name=tem_product[x].product_name,
                sku=auto_code,
                color=tem_product[x].color,
                size=tem_product[x].size,
                avail_quantity=0,
                created_at=DateTime
            )
            parent = super().create(validated_data)
            add_stock.save()
            tem_product[x].delete()

        return parent

    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        parent = super().update(instance, validated_data)
        return parent


### ATTRIBUTE SERIALIZER
class VariationGroupSerializer(serializers.Serializer):
    att_type = serializers.CharField(required=False)
    attribute_name = serializers.CharField(required=False)
    variation = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):

        get_attribute_name = validated_data.get('attribute_name')
        get_variations = validated_data.get('variation')
        get_att_type = validated_data.get('att_type')
        try:
            attt_type = AttributeType.objects.get(id=get_att_type)
            get_attribute_type_id = attt_type.id
        except:
            return Response("Incorrect Attribute Type ID")
        try:
            get_all_attribute = Attribute.objects.get(attribute_name=get_attribute_name)
            if get_attribute_name in get_all_attribute.attribute_name:
                get_attribute_id = Attribute.objects.get(attribute_name=get_attribute_name).id
        except:
            attribute = Attribute(
                attribute_name=get_attribute_name,
                att_type_id=get_attribute_type_id,
                status="active",
                created_at=DateTime,
            )
            attribute.save()
        get_attribute_id = Attribute.objects.get(attribute_name=get_attribute_name).id

        if len(get_variations) > 0:
            for variations in range(len(get_variations)):
                try:
                    variation = Variation.objects.filter(attribute_name_id=get_attribute_id)
                    if get_variations[variations] in variation[variations].variation_name:
                        pass
                except:
                    variation = Variation(
                        variation_name=get_variations[variations],
                        attribute_name_id=get_attribute_id,
                        status="active",
                        created_at=DateTime,
                    )
                    variation.save()
        return validated_data

# class VariationGroupSerializer(serializers.Serializer):
#     att_type = serializers.CharField(required=False)
#     attribute_name = serializers.CharField(required=False)
#     variation = serializers.ListField(child=serializers.CharField())

#     def create(self, validated_data):

#         get_attribute_name = validated_data.get('attribute_name')
#         get_variations = validated_data.get('variation')
#         get_att_type = validated_data.get('att_type')
#         try:
#             get_all_att_type = AttributeType.objects.get(att_type=get_att_type)
#             if get_att_type in get_all_att_type.att_type:
#                 get_attribute_type_id = AttributeType.objects.get(att_type=get_att_type).id
#         except:

#             attribute_type = AttributeType(
#                 att_type=get_att_type,
#                 status="active",
#                 created_at=DateTime,
#             )
#             attribute_type.save()

#         get_attribute_type_id = AttributeType.objects.get(att_type=get_att_type).id
#         try:
#             get_all_attribute = Attribute.objects.get(attribute_name=get_attribute_name)
#             if get_attribute_name in get_all_attribute.attribute_name:
#                 get_attribute_id = Attribute.objects.get(attribute_name=get_attribute_name).id
#         except:
#             attribute = Attribute(
#                 attribute_name=get_attribute_name,
#                 att_type_id=get_attribute_type_id,
#                 status="active",
#                 created_at=DateTime,
#             )
#             attribute.save()
#         get_attribute_id = Attribute.objects.get(attribute_name=get_attribute_name).id
#         if len(get_variations) > 0:
#             for variations in range(len(get_variations)):
#                 variation = Variation(
#                     variation_name=get_variations[variations],
#                     attribute_name_id=get_attribute_id,
#                     status="active",
#                     created_at=DateTime,
#                 )
#                 variation.save()
#         return validated_data
