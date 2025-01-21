from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    no_of_outlets = models.IntegerField(null=True)
    no_of_registered_outlets = models.IntegerField(null=True)
    class Meta:
        db_table = 'tbl_shops'
    def __str__(self):
        return self.name