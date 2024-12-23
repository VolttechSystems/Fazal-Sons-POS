from rest_framework.serializers import *
from AppPOS.models import * 

class TransactionSerializer(ModelSerializer):
   
    class Meta:
        model = Transaction
        fields = "__all__"        
        # fields = ['invoice_code', 'created_at', 'outlet_code', 'cust_code']        