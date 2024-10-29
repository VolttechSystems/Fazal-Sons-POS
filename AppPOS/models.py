from django.db import models
from AppCustomer.models import *
from AppProduct.models import *
# Create your models here.

class PurchaseInvoice(models.Model):
    invoice_code = models.CharField(max_length=100, null=True, unique=True) # auto generated
    status = models.CharField(null=True, blank=True)
    purchase_date = models.CharField(null=True, blank=True)
    payment_type = models.CharField(null=True, blank=True)
    invoice_amount = models.CharField(null=True, blank=True)
    discount = models.CharField(null=True, blank=True)
    grand_total = models.CharField(null=True, blank=True)
    cust_code = models.ForeignKey(Customer, to_field='cust_code', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_purchase_invoice'

    def __str__(self):
        return self.invoice_code
    

class PurchaseInvoiceItem(models.Model):
    invoice_code = models.ForeignKey(PurchaseInvoice, to_field='invoice_code', on_delete=models.CASCADE, null=True, blank=True)
    sku = models.ForeignKey(Product, to_field='sku', on_delete=models.CASCADE, null=True, blank=True)
    invoice_item_code = models.CharField(max_length=100, null=True, unique=True)
    status = models.CharField(null=True, blank=True)
    quantity = models.CharField(null=True, blank=True)
    cost = models.CharField(null=True, blank=True)
    item_total = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    class Meta:
        db_table = 'tbl_purchase_invoice_item'

    def __str__(self):
        return self.invoice_code
