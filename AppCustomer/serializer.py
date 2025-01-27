from rest_framework.serializers import ModelSerializer
from .models import *
import datetime
from .utils import *

DateTime = datetime.datetime.now()

### CUSTOMER CHANNEL SERIALIZER
class CustomerChannelSerializer(ModelSerializer):
    class Meta:
        model = CustomerChannel
        fields = ['id', 'customer_channel', 'shop']

    def create(self, validated_data):
        validated_data['cus_ch_code'] = AutoGenerateCodeForModel(CustomerChannel, 'cus_ch_code', 'CCH-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['created_by'] = request.user.username
        cust_channel = super().create(validated_data)
        return cust_channel

    def update(self, instance, validated_data):
        cust_channel = super().update(instance, validated_data)
        cust_channel.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     cust_channel.updated_by = request.user.username
        cust_channel.save()
        return cust_channel


### CUSTOMER TYPE SERIALIZER
class CustomerTypeSerializer(ModelSerializer):
    class Meta:
        model = CustomerType
        fields = ['id', 'customer_type' , 'shop']

    def create(self, validated_data):
        validated_data['cus_type_code'] = AutoGenerateCodeForModel(CustomerType, 'cus_type_code', 'CTP-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['created_by'] = request.user.username
        cust_type = super().create(validated_data)
        return cust_type

    def update(self, instance, validated_data):
        cust_type = super().update(instance, validated_data)
        cust_type.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     cust_type.updated_by = request.user.username
        cust_type.save()
        return cust_type

### CUSTOMER SERIALIZER
class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer

        fields = [
            'id','cust_code', 'customer_channel', 'customer_type',  'display_name', 'gender',
            'company_name', 'email', 'mobile_no', 'international_no', 'landline_no', 'password', 'address',
            'shipping_address', 'city', 'zip_code', 'province', 'country', 'internal_note', 'image', 'online_access',
            'status', 'shop', 'outlet']

    def create(self, validated_data):
        
        get_display_name = validated_data.get('display_name')
        split_name = get_display_name.split(' ')
        validated_data['first_name'] =  split_name[0]
        validated_data['last_name'] =  split_name[1] if len(split_name) > 1 else None
        
        validated_data['cust_code'] = AutoGenerateCodeForModel(Customer, 'cust_code', 'CUST-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime    
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     validated_data['created_by']  = request.user.username
        customer = super().create(validated_data)
        customer.updated_at = None
        return customer

    def update(self, instance, validated_data):
        get_display_name = validated_data.get('display_name')
        split_name = get_display_name.split(' ')
    
        customer = super().update(instance, validated_data)
        customer.first_name = split_name[0]
        customer.last_name =  split_name[1] if len(split_name) > 1 else None
        customer.updated_at = DateTime
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
                     customer.updated_by = request.user.username
        customer.save()
        return customer
