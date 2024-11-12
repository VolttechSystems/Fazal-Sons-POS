from rest_framework.serializers import ModelSerializer
from .models import *
import datetime
from .utils import *

DateTime = datetime.datetime.now()

### CUSTOMER CHANNEL SERIALIZER
class CustomerChannelSerializer(ModelSerializer):
    class Meta:
        model = CustomerChannel

        fields = ('id', 'customer_channel',)

    def create(self, validated_data):
        validated_data['cus_ch_code'] = AutoGenerateCodeForModel(CustomerChannel, 'cus_ch_code', 'CCH-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        cust_channel = super().create(validated_data)
        return cust_channel

    def update(self, instance, validated_data):
        cust_channel = super().update(instance, validated_data)
        cust_channel.updated_at = DateTime
        cust_channel.save()
        return cust_channel

### CUSTOMER TYPE SERIALIZER
class CustomerTypeSerializer(ModelSerializer):
    class Meta:
        model = CustomerType

        fields = ('id', 'customer_type',)

    def create(self, validated_data):
        validated_data['cus_type_code'] = AutoGenerateCodeForModel(CustomerType, 'cus_type_code', 'CTP-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        cust_type = super().create(validated_data)
        return cust_type

    def update(self, instance, validated_data):
        cust_type = super().update(instance, validated_data)
        cust_type.updated_at = DateTime
        cust_type.save()
        return cust_type

### CUSTOMER SERIALIZER
class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer

        fields = (
            'id', 'customer_channel', 'customer_type', 'first_name', 'first_name', 'last_name', 'display_name', 'gender',
            'company_name', 'email', 'mobile_no', 'international_no', 'landline_no', 'password', 'address',
            'shipping_address', 'city', 'zip_code', 'province', 'country', 'internal_note', 'image', 'online_access',
            'status')

    def create(self, validated_data):
        validated_data['cust_code'] = AutoGenerateCodeForModel(Customer, 'cust_code', 'CUST-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        customer = super().create(validated_data)
        customer.updated_at = None
        return customer

    def update(self, instance, validated_data):
        customer = super().update(instance, validated_data)
        customer.updated_at = DateTime
        customer.save()
        return customer
