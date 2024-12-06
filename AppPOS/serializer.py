import datetime
from rest_framework import serializers
from .models import *
from AppCustomer.utils import *
from rest_framework.response import Response
from AppCustomer.utils import *
from AppAccount.admin import *

DateTime = datetime.datetime.now()

### TRANSACTION SERIALIZER
class AdditionalFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFee
        fields = ['id','fee_code','fee_name']

    def create(self, validated_data):
        validated_data['fee_code'] = AutoGenerateCodeForModel(AdditionalFee, 'fee_code', 'FEE-')
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        fee = super().create(validated_data)
        return fee

    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        fee = super().update(instance, validated_data)
        return fee


### ADDITIONAL FEE SERIALIZER
class TransactionItemSerializer(serializers.ModelSerializer):
    cust_code = serializers.CharField(required=False)
    saleman_code = serializers.CharField(required=False)
    overall_discount = serializers.CharField(required=False)
    # item_discount = serializers.CharField(required=False)
    outlet_code = serializers.CharField(required=False)
    additional_fee_code = serializers.CharField(required=False, allow_blank=True)
    additional_fee = serializers.CharField(required=False, allow_blank=True)
    advanced_payment = serializers.CharField(required=False, allow_blank=True)
    sku = serializers.ListField(child=serializers.CharField())
    quantity = serializers.ListField(child=serializers.CharField())
    rate = serializers.ListField(child=serializers.CharField())
    item_discount = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = TransactionItem
        fields = "__all__"
      
    def create(self, validated_data):
        get_sku = validated_data.get('sku')
        get_quantity = validated_data.get('quantity')
        get_rate = validated_data.get('rate')
        get_customer = validated_data.get('cust_code')
        get_saleman_code = validated_data.get('saleman_code')
        get_overall_discount = validated_data.get('overall_discount')
        get_item_discount = validated_data.get('item_discount')
        get_outlet_code = validated_data.get('outlet_code')
        get_additional_fee_code = validated_data.get('additional_fee_code')
        get_additional_fee = validated_data.get('additional_fee')
        get_advanced_payment = validated_data.get('advanced_payment')

        # get_sku = get_sku.replace("'", "")
        # get_sku = get_sku.replace("[", "")
        # get_sku = get_sku.replace("]", "")
        # get_sku = get_sku.split(",")
        len_sku = len(get_sku)

        # get_quantity = get_quantity.replace("'", "")
        # get_quantity = get_quantity.replace("[", "")
        # get_quantity = get_quantity.replace("]", "")
        # get_quantity = get_quantity.split(",")

        # get_rate = get_rate.replace("'", "")
        # get_rate = get_rate.replace("[", "")
        # get_rate = get_rate.replace("]", "")
        # get_rate = get_rate.split(",")

        # get_item_discount = get_item_discount.replace("'", "")
        # get_item_discount = get_item_discount.replace("[", "")
        # get_item_discount = get_item_discount.replace("]", "")
        # get_item_discount = get_item_discount.split(",")
        len_additional_fee_code = 0
        if get_additional_fee_code != '':
            # get_additional_fee_code = get_additional_fee_code.replace("'", "")
            # get_additional_fee_code = get_additional_fee_code.replace("[", "")
            # get_additional_fee_code = get_additional_fee_code.replace("]", "")
            # get_additional_fee_code = get_additional_fee_code.split(",")
            len_additional_fee_code = len(get_additional_fee_code)

        # get_additional_fee = get_additional_fee.replace("'", "")
        # get_additional_fee = get_additional_fee.replace("[", "")
        # get_additional_fee = get_additional_fee.replace("]", "")
        # get_additional_fee = get_additional_fee.split(",")

        if len_sku > 0:
            invoice_auto_code = AutoGenerateCodeForModel(Transaction, 'invoice_code', 'INV-')
            transaction = Transaction(
                invoice_code=invoice_auto_code,
                cust_code_id=get_customer,
                salesman_code_id=get_saleman_code,
                created_at=DateTime,
                outlet_code_id=get_outlet_code
            )
            transaction.save()

            Total_quantity = 0
            Gross_total = 0
            item_wise_discount = 0
            Grand_total = 0
            total_discount = 0
            due_amount = 0

            for item in range(len_sku):
                invoice_item_auto_code = AutoGenerateCodeForModel(TransactionItem, 'invoice_item_code', 'IIT-')
                quantity = int(get_quantity[item])
                rate = int(get_rate[item])
                sku = get_sku[item].strip()
                item_gross_total = quantity * rate
                item_discount_per = int(get_item_discount[item].strip())
                item_discount = int(item_discount_per * item_gross_total / 100)
                item_total = item_gross_total - item_discount

                transaction_item = TransactionItem(
                    invoice_code_id=invoice_auto_code,
                    sku=sku,
                    invoice_item_code=invoice_item_auto_code,
                    quantity=quantity,
                    rate=rate,
                    gross_total=item_gross_total,
                    per_discount=item_discount_per,
                    discounted_value=item_discount,
                    item_total=item_total,
                    created_at=DateTime
                )
                transaction_item.save()
                Total_quantity += quantity
                Gross_total += int(item_gross_total)
                item_wise_discount += int(item_discount)
            ## Update Transaction
            item_discounted_amount = Gross_total - item_wise_discount
            if get_overall_discount != 0:
                discount_amount = int(int(get_overall_discount) * item_discounted_amount / 100)
                Grand_total = int(item_discounted_amount - discount_amount)
                total_discount = discount_amount + item_wise_discount

            transaction = Transaction.objects.get(invoice_code=invoice_auto_code)

            transaction.quantity = Total_quantity
            transaction.gross_total = Gross_total
            transaction.per_discount = get_overall_discount
            transaction.discounted_value = total_discount
            transaction.items_discount = item_wise_discount
            transaction.payment_type = "Cash"
            ## ADD ADDITIONAL FEE
            total_additional_fee = 0
            if len_additional_fee_code > 0:
                for x in range(len_additional_fee_code):
                    fee_code = get_additional_fee_code[x].strip()
                    additional_fee = AdditionalFee.objects.get(fee_code=fee_code)

                    transaction_additional_fee = FeeRecord(
                        fee_type_id=additional_fee.id,
                        transaction_id_id=transaction.id,
                        fee=get_additional_fee[x],
                    )
                    transaction_additional_fee.save()
                    total_additional_fee += int(get_additional_fee[x])

            grand_total_with_fee = Grand_total + total_additional_fee
            transaction.additional_fees = total_additional_fee
            transaction.grand_total = grand_total_with_fee

            if int(get_advanced_payment) != 0:
                due_amount = int(grand_total_with_fee) - int(get_advanced_payment)
                transaction.advanced_payment = get_advanced_payment
                transaction.due_amount = due_amount
                transaction.status = "unpaid"
            else:
                transaction.advanced_payment = 0
                transaction.due_amount = 0
                transaction.status = "paid"

            transaction.save()

        return validated_data


### SALESMAN SERIALIZER
class AddSalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = ['id', 'salesman_code','salesman_name', 'wholesale_commission', 'retail_commission', 'token_commission', 'outlet_code']

    def create(self, validated_data):
        get_checkBox_value = self.context['request'].data['CheckBoxValue']

        validated_data['salesman_code'] = AutoGenerateCodeForModel(Salesman, 'salesman_code', 'SL-')
        if get_checkBox_value == 'true':
            get_salesman_commision = salesman_commission
            validated_data['wholesale_commission'] = str(get_salesman_commision['wholesale_commission'])
            validated_data['retail_commission'] = str(get_salesman_commision['retail_commission'])
            validated_data['token_commission'] = str(get_salesman_commision['token_commission'])
        validated_data['updated_at'] = None
        validated_data['created_at'] = DateTime
        salesman = super().create(validated_data)
        return salesman

    def update(self, instance, validated_data):
        validated_data['updated_at'] = DateTime
        salesman = super().update(instance, validated_data)
        return validated_data


### TRANSACTION RETURN SERIALIZER
class TransactionReturnSerializer(serializers.ModelSerializer):
    sku = serializers.ListField(child=serializers.CharField())
    rate = serializers.ListField(child=serializers.CharField())
    quantity = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = TransactionReturn
        fields = '__all__'
        
    def create(self, validated_data):
        get_sku = validated_data.get('sku')
        get_rate = validated_data.get('rate')
        get_quantity = validated_data.get('quantity')
        invoice_code = validated_data.get('invoice_code')
        # print(len(get_quantity))
        
        if len(get_sku) > 0:
            for i in range(len(get_sku)):
                validated_data['sku'] = get_sku[i]
                validated_data['rate'] = get_rate[i]
                validated_data['quantity'] = get_quantity[i]
                validated_data['total_amount'] = int(get_quantity[i]) * int(get_rate[i])
                validated_data['updated_at'] = None
                validated_data['created_at'] = DateTime
                sales_return = super().create(validated_data)
                update_transaction_status = TransactionItem.objects.get(sku=get_sku[i], invoice_code_id= invoice_code)
                update_transaction_status.status = 'return'
                update_transaction_status.updated_at = DateTime
                update_transaction_status.save()
        return sales_return
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product_name', 'sku','cost_price', 'selling_price', 'description']