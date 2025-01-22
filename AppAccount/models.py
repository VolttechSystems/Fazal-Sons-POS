from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from AppProduct.models import Outlet
from AppAdmin.models import Shop
from django.utils.timezone import now


class CustomPermissions(models.Model):
    permission_name = models.CharField(max_length=200, null=False, unique=True)

    class Meta:
        db_table = 'tbl_role_permission'

    def __str__(self):
        return self.permission_name
    

class SystemRole(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    permissions = models.ManyToManyField('CustomPermissions', related_name='roles')
    sys_role_name = models.CharField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True) # Active, BLock
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_system_role'
        unique_together = ('shop', 'sys_role_name' )

    def __str__(self):
        return self.sys_role_name



class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    system_roles = models.ManyToManyField(SystemRole, related_name='users')
    outlet = models.ManyToManyField(Outlet, related_name='outlet_users')
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        db_table = "tbl_user_profile"
        # unique_together = ('user', 'shop')

    def __str__(self):
        return self.user.username
    
    


    