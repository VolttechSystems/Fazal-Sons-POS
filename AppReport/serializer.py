from rest_framework.serializers import *
from AppPOS.models import * 

class TransactionSerializer(ModelSerializer):
   
    class Meta:
        model = Transaction
        fields = "__all__"        

class SalesmanSerializer(ModelSerializer):
     class Meta:
        model = Salesman
        fields = ['salesman_name', 'salesman_code']   
