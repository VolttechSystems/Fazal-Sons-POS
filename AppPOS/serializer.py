import datetime

from rest_framework import serializers
from .models import *
from AppCustomer.utils import *
from rest_framework.response import Response

DateTime = datetime.datetime.now()


class TransactionItemSerializer(serializers.ModelSerializer):
    cust_code = serializers.CharField(required=False)
    discount = serializers.CharField(required=False)

    class Meta:
        model = TransactionItem
        fields = "__all__"

    def create(self, validated_data):
        get_sku = validated_data.get('sku')
        get_quantity = validated_data.get('quantity')
        get_rate = validated_data.get('rate')
        get_customer = validated_data.get('cust_code')
        get_discount = validated_data.get('discount')
        # get_additional_fees = validated_data.get('additional_fees')
        # get_payment_type = validated_data.get('payment_type')

        get_sku = get_sku.replace("'", "")
        get_sku = get_sku.replace("[", "")
        get_sku = get_sku.replace("]", "")
        get_sku = get_sku.split(",")
        len_sku = len(get_sku)

        get_quantity = get_quantity.replace("'", "")
        get_quantity = get_quantity.replace("[", "")
        get_quantity = get_quantity.replace("]", "")
        get_quantity = get_quantity.split(",")
        len_quantity = len(get_quantity)

        get_rate = get_rate.replace("'", "")
        get_rate = get_rate.replace("[", "")
        get_rate = get_rate.replace("]", "")
        get_rate = get_rate.split(",")
        len_rate = len(get_rate)

        if len_sku > 0:
            invoice_auto_code = AutoGenerateCodeForModel(Transaction, 'invoice_code', 'INV-')
            transaction = Transaction(
                invoice_code=invoice_auto_code,
                cust_code_id=get_customer,
                created_at=DateTime
            )
            transaction.save()
            Total_quatity = 0
            Gross_total = 0
            for item in range(len_sku):
                invoice_item_auto_code = AutoGenerateCodeForModel(TransactionItem, 'invoice_item_code', 'IIT-')
                quantity = int(get_quantity[item])
                rate = int(get_rate[item])
                sku = get_sku[item].strip()
                gross_total = quantity * rate

                transaction_item = TransactionItem(
                    invoice_code_id=invoice_auto_code,
                    sku=sku,
                    invoice_item_code=invoice_item_auto_code,
                    quantity=quantity,
                    rate=rate,
                    gross_total=gross_total,
                    # per_discount=gross_total,
                    # discounted_value=gross_total,
                    item_total=gross_total
                )
                transaction_item.save()
                Total_quatity += quantity
                Gross_total += int(gross_total)
            # Update Transaction
            Discounted_value = int(int(get_discount) * Gross_total / 100)
            Grand_total = int(Gross_total - Discounted_value)

            transaction = Transaction.objects.get(invoice_code=invoice_auto_code)
            transaction.quantity = Total_quatity
            transaction.gross_total = Gross_total
            transaction.per_discount = get_discount
            transaction.discounted_value = Discounted_value
            transaction.grand_total = Grand_total
            # transaction.advanced_payment = Total_quatity
            # transaction.due_amount = Total_quatity
            transaction.save()
        response = "Transaction Created"

        return response
