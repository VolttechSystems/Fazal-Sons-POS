from django.db import models
from AppCustomer.models import *
from AppProduct.models import *



# Create your models here.

class Transaction(models.Model):
    invoice_code = models.CharField(max_length=100, null=True, unique=True)  # auto generated
    cust_code = models.ForeignKey(Customer, to_field='cust_code', on_delete=models.CASCADE, null=True,
                                  blank=True)  # customer code
    # salesman  = models.CharField(null=True, blank=True)
    quantity = models.CharField(null=True, blank=True)
    gross_total = models.CharField(null=True, blank=True)  # Sum of all product prices without any discounts
    per_discount = models.CharField(null=True, blank=True)  # Discount in %
    discounted_value = models.CharField(null=True, blank=True)  # Discount in RS
    grand_total = models.CharField(null=True,
                                   blank=True)  # Final amount payable after applying discounts, fees, and any advance payments.
    advanced_payment = models.CharField(null=True, blank=True)
    due_amount = models.CharField(null=True,
                                  blank=True)  # If the customer makes a partial payment, the system will calculate the due amount to be paid later.
    additional_fees = models.CharField(null=True, blank=True)
    # purchase_date = models.CharField(null=True, blank=True)
    payment_type = models.CharField(null=True, blank=True)
    status = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_transaction'

    def __str__(self):
        return self.invoice_code


class TransactionItem(models.Model):
    invoice_code = models.ForeignKey(Transaction, to_field='invoice_code', on_delete=models.CASCADE, null=True,
                                     blank=True)
    sku = models.CharField(null=True, blank=True)
    invoice_item_code = models.CharField(max_length=100, null=True, unique=True)
    quantity = models.CharField(null=True, blank=True)
    rate = models.CharField(null=True, blank=True)
    gross_total = models.CharField(null=True, blank=True)
    per_discount = models.CharField(null=True, blank=True)
    discounted_value = models.CharField(null=True, blank=True)
    item_total = models.CharField(null=True, blank=True)
    status = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tbl_transaction_item'

    def __str__(self):
        return self.invoice_item_code
