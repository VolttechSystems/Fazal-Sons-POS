from django.db import models

# Create your models here.

# class Salesman(models.Model):
#     salesman_code = models.CharField(max_length=100, null=True, unique=True) # SL-1
#     salesman_name = models.CharField(max_length=100, null=True, blank=True)
#     # outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
#     outlet = models.ManyToManyField(Outlet, through='SalesmanOutlet')
#     wholesale_commission = models.CharField(max_length=100, null=True, blank=True)
#     retail_commission = models.CharField(max_length=100, null=True, blank=True)
#     token_commission = models.CharField(max_length=100, null=True, blank=True)
#     status = models.CharField(null=True, blank=True)  
#     created_at = models.DateTimeField(null=True)
#     created_by = models.CharField(max_length=200, null=True)
#     updated_at = models.DateTimeField(null=True)
#     updated_by = models.CharField(max_length=200, null=True)

#     class Meta:
#         db_table = 'tbl_salesman'

#     def __str__(self):
#         return self.salesman_code

class ShopOwner(models.Model):
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    no_of_outlets = models.IntegerField(null=True)
    no_of_registered_outlets = models.IntegerField(null=True)
    class Meta:
        db_table = 'tbl_shop_owner'
    def __str__(self):
        return self.name