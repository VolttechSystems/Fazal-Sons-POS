from rest_framework import serializers
from AppProduct.models import *
import datetime
from django.utils import timezone
from AppCustomer.utils import *
from AppStock.models import *
from rest_framework import status
from rest_framework.response import Response
from itertools import product
import ast
import json

DateTime = datetime.datetime.now()

### GET FIRST CHARACTER OF EACH WORD
def get_initials(name):
    name = "".join([word[0] for word in name.split()])
    return name.upper()
### GET FIRST THREE CHARACTER OF WORD
def get_first_three_of_first_word(name):  # Check if the string contains spaces
    name = name.split()[0][:3]  # Get the first word and slice the first three characters
    return name.upper()


### OUTLET SERIALIZER
class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ['id', 'outlet_code', 'outlet_name', 'address', 'outlet_mobile', 'manager_name', 'contact_number', 'shop']
        
    def validate(self, validate_data):
       shop =  validate_data.get('shop')
       allowed_outlets = shop.no_of_outlets
       outlet = Outlet.objects.filter(shop_id=shop.id)
       if int(len(outlet)) >= int(allowed_outlets):
           raise serializers.ValidationError("You Cannot add More Outlets. Your Allowed Limit is Full")
       return validate_data
           

    def create(self, validated_data):
        outlet = super().create(validated_data)
        outlet.updated_at = None
        outlet.created_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     outlet.created_by = request.user.username

        outlet.save()
        return outlet

    def update(self, instance, validated_data):
        outlet = super().update(instance, validated_data)
        outlet.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     outlet.updated_by = request.user.username
        outlet.save()
        return outlet


### BRAND SERIALIZER
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','brand_name', 'symbol', 'description', 'status', 'shop']

    def create(self, validated_data):
        brand = super().create(validated_data)
        brand.updated_at = None
        brand.created_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     brand.created_by = request.user.username
        brand.save()
        return brand

    def update(self, instance, validated_data):
        brand = super().update(instance, validated_data)
        brand.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     brand.updated_by = request.user.username
        brand.save()
        return brand


### ATTRIBUTE TYPE SERIALIZER
class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeType
        fields = ['id', 'att_type', 'status', 'shop']

    def create(self, validated_data):
        attr_type = super().create(validated_data)
        attr_type.updated_at = None
        attr_type.created_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     attr_type.created_by = request.user.username
        attr_type.save()
        return attr_type

    def update(self, instance, validated_data):
        attr_type = super().update(instance, validated_data)
        attr_type.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     attr_type.updated_by = request.user.username
        attr_type.save()
        return attr_type

### HEAD CATEGORY SERIALIZER
class HeadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadCategory
        fields = ['id', 'hc_name', 'symbol', 'description', 'status', 'shop']

    def create(self, validated_data):
        h_category = super().create(validated_data)
        h_category.created_at = DateTime
        h_category.updated_at = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     h_category.created_by = request.user.username
        h_category.save()
        return h_category

    def update(self, instance, validated_data):
        h_category = super().update(instance, validated_data)
        h_category.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     h_category.updated_by = request.user.username
        h_category.save()
        return h_category


### PARENT CATEGORY SERIALIZER
class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = ['id', 'pc_name', 'symbol', 'description', 'status', 'hc_name', 'shop']

    def create(self, validated_data):
        p_category = super().create(validated_data)
        p_category.created_at = DateTime
        p_category.updated_at = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     p_category.created_by = request.user.username
        p_category.save()
        return p_category

    def update(self, instance, validated_data):
        p_category = super().update(instance, validated_data)
        p_category.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     p_category.updated_by = request.user.username
        p_category.save()
        return p_category

## CATEGORY SERIALIZER
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
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['created_by']= request.user.username
        category = super().create(validated_data)
        return category

    def update(self, instance, validated_data):
        get_subcategory_option = validated_data.get('subcategory_option')
        if get_subcategory_option == 'True':
            validated_data['attribute_group'] = []
        validated_data['updated_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['updated_by']= request.user.username
        category = super().update(instance, validated_data)
        return category


## SUB CATEGORY SERIALIZER
class SubCategorySerializer(serializers.ModelSerializer):
    attribute_group = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = SubCategory
        fields = '__all__'

    def create(self, validated_data):
        validated_data['created_at'] = DateTime
        validated_data['updated_at'] = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['created_by']= request.user.username
        subcategory = super().create(validated_data)
        return subcategory

    def update(self, instance, validated_data):
        validated_data['created_at'] = DateTime
        validated_data['updated_at'] = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['updated_by']= request.user.username
        sub_category = super().update(instance, validated_data)
        return sub_category

### TEMPORARY PRODUCT SERIALIZER
class TempProductSerializer(serializers.ModelSerializer):
    color = serializers.CharField(required=False)
    variations = serializers.CharField(required=False)

    class Meta:
        model = TemporaryProduct
        fields = '__all__'

    def validate(self, data):
        """
        Check if the specification already exists in the description.
        """
        get_variations = data.get('variations')
        get_color = data.get('color')
        parsed_color = ast.literal_eval(get_color)
        parsed_variations = json.loads(get_variations)
        initial_variations = list(product(*parsed_variations))

        for variation in initial_variations:
            all_variation = list(variation)
            specs = "-".join(map(str, all_variation))
            for color in parsed_color:
                if TemporaryProduct.objects.filter(description__iexact=specs, color__iexact=color).exists():
                    raise serializers.ValidationError("The specification " + specs + "-" + color + " is already added.")
        return data

    def create(self, validated_data):
        parent = ''
        get_color = validated_data.get('color')
        get_color = ast.literal_eval(get_color)
        get_variations = validated_data.pop('variations', None)
        get_variations = ast.literal_eval(get_variations)
        outlet = validated_data.get('outlet')
        brand = validated_data.get('brand')
        shop_id = validated_data.get('shop')
        print(shop_id)
        if len(get_variations) > 0:

            initial_variations = list(product(*get_variations))
            outlet_code = "OT"
            brand_code = "BR"
            if outlet != None:
                    if " " in outlet.outlet_name:
                        outlet_code = get_initials(outlet.outlet_name)
                    else:
                        outlet_code = get_first_three_of_first_word(outlet.outlet_name)
                    if brand != None:
                        if " " in brand.brand_name:
                            brand_code = get_initials(brand.brand_name)
                        else:
                            brand_code = get_first_three_of_first_word(brand.brand_name)
            sku_code = outlet_code + "-" + brand_code
            if len(get_color) > 0:

                for color in range(len(get_color)):
                        for variation in initial_variations:
                            all_variation = list(variation)
                            specs = "-".join(map(str, all_variation))
                            auto_sku_code = AutoGenerateCodeForModel(TemporaryProduct, 'sku', sku_code + '-')
                            validated_data['sku'] = auto_sku_code
                            validated_data['color'] = get_color[color]
                            validated_data['description'] = specs
                            validated_data['created_at'] = DateTime
                            request = self.context.get('request')
                            if request and hasattr(request, 'user'):
                                        validated_data['created_by']= request.user.username
                            parent = super().create(validated_data)
            else:
                for variation in initial_variations:
                    auto_sku_code = AutoGenerateCodeForModel(TemporaryProduct, 'sku', sku_code + '-')
                    validated_data['sku'] = auto_sku_code
                    validated_data['color'] = ""
                    all_variation = list(variation)
                    specs = "-".join(map(str, all_variation))
                    validated_data['description'] = specs
                    validated_data['created_at'] = DateTime
                    request = self.context.get('request')
                    if request and hasattr(request, 'user'):
                            validated_data['created_by']= request.user.username
                    parent = super().create(validated_data)
        return parent

    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                validated_data['updated_by']= request.user.username
        parent = super().update(instance, validated_data)
        return parent

### PRODUCT SERIALIZER
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def validate_image(self, value):
    #         # Add any custom validation for the image field here
    #         if value.size > 2 * 1024 * 1024:  # Example: Max 2 MB size
    #             raise serializers.ValidationError("Image size should not exceed 2 MB.")
    #         return value

    def create(self, validated_data):
        parent = ''
        # Access the request from the context
        request = self.context.get('request')
        # Get the URL parameter
        shop_id = request.parser_context['kwargs'].get('shop')
        tem_product = TemporaryProduct.objects.filter(shop_id=shop_id)
        len_tem_product = len(tem_product)
        for x in range(len_tem_product):
            outlet = tem_product[x].outlet
            brand = tem_product[x].brand
            outlet_code = "OT"
            brand_code = "BR"
            if outlet != None:
                    if " " in outlet.outlet_name:
                        outlet_code = get_initials(outlet.outlet_name)
                    else:
                        outlet_code = get_first_three_of_first_word(outlet.outlet_name)
            if brand != None:
                        if " " in brand.brand_name:
                            brand_code = get_initials(brand.brand_name)
                        else:
                            brand_code = get_first_three_of_first_word(brand.brand_name)
                        
            sku_code = outlet_code + "-" + brand_code
            auto_sku_code = AutoGenerateCodeForModel(Product, 'sku', sku_code + '-')
            validated_data['product_name'] = tem_product[x].product_name
            validated_data['sku'] = auto_sku_code
            validated_data['outlet'] = tem_product[x].outlet
            validated_data['sub_category'] = tem_product[x].sub_category
            validated_data['category'] = tem_product[x].category
            validated_data['brand'] = tem_product[x].brand
            validated_data['season'] = tem_product[x].season
            validated_data['description'] = tem_product[x].description
            validated_data['notes'] = tem_product[x].notes
            validated_data['color'] = tem_product[x].color
            validated_data['image'] = tem_product[x].image
            validated_data['cost_price'] = tem_product[x].cost_price
            validated_data['selling_price'] = tem_product[x].selling_price
            validated_data['discount_price'] = tem_product[x].discount_price
            validated_data['wholesale_price'] = tem_product[x].wholesale_price
            validated_data['retail_price'] = tem_product[x].retail_price
            validated_data['token_price'] = tem_product[x].token_price
            validated_data['created_at'] = DateTime
            validated_data['created_by'] = tem_product[x].created_by
            validated_data['shop_id'] = tem_product[x].shop_id
            # Add Stock
            add_stock = Stock(
                shop_id=shop_id,
                product_name=tem_product[x].product_name,
                sku=auto_sku_code,
                color=tem_product[x].color,
                avail_quantity=0,
                created_at=DateTime
            )
            parent = super().create(validated_data)
            add_stock.save()
            tem_product[x].delete()

        return parent

    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        print(validated_data['sku'])
        Update_stock = Stock.objects.get(sku=validated_data['sku'])
        Update_stock.product_name = validated_data['product_name'] 
        Update_stock.save()
        parent = super().update(instance, validated_data)
        return parent
class ShowAllProductSerializer(serializers.ModelSerializer):
    outlet = serializers.StringRelatedField()  
    brand = serializers.StringRelatedField()  
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'outlet', 'brand', 'shop']


### ATTRIBUTE SERIALIZER
class VariationGroupSerializer(serializers.Serializer):
    att_type = serializers.CharField(required=False)
    attribute_name = serializers.CharField(required=False)
    shop = serializers.CharField(required=False)
    variation = serializers.ListField(child=serializers.CharField())
    
    

    def create(self, validated_data):

        get_attribute_name = validated_data.get('attribute_name')
        get_variations = validated_data.get('variation')
        get_att_type = validated_data.get('att_type')
        get_shop = validated_data.get('shop')
        request = self.context.get('request')
        try:
            att_type = AttributeType.objects.get(shop_id=get_shop,id=get_att_type)
            get_attribute_type_id = att_type.id
        except:
            return Response("Incorrect Attribute Type ID")
        try:
            get_all_attribute = Attribute.objects.get(shop_id=get_shop, attribute_name=get_attribute_name)
            if get_attribute_name in get_all_attribute.attribute_name:
                get_attribute_id = Attribute.objects.get(shop_id=get_shop, attribute_name=get_attribute_name).id
        except:
            attribute = Attribute(
                attribute_name=get_attribute_name,
                att_type_id=get_attribute_type_id,
                shop_id=get_shop,
                status="active",
                created_at=DateTime,
                created_by=request.user.username
        
            )
            attribute.save()
        get_attribute_id = Attribute.objects.get(shop_id=get_shop, attribute_name=get_attribute_name).id

        if len(get_variations) > 0:
            for variations in range(len(get_variations)):
                try:
                    variation = Variation.objects.filter(shop_id=get_shop, attribute_name_id=get_attribute_id)
                    if get_variations[variations] in variation[variations].variation_name:
                        pass
                except:
                    variation = Variation(
                        variation_name=get_variations[variations],
                        attribute_name_id=get_attribute_id,
                        shop_id=get_shop,
                        status="active",
                        created_at=DateTime,
                         created_by=request.user.username
        
                    )
                    variation.save()
        return validated_data
