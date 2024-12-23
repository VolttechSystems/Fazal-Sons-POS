from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Permissions(models.Model):
    permission_name = models.CharField(max_length=200, null=False, unique=True)

    class Meta:
        db_table = 'tbl_role_permission'

    def __str__(self):
        return self.permission_name
    

class SystemRole(models.Model):
    permissions = models.ManyToManyField('Permissions', related_name='roles')
    sys_role_name = models.CharField(max_length=200, null=True)  # Changed to CharField for consistency
    status = models.TextField(max_length=200, null=True) # Active, BLock
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_system_role'

    def __str__(self):
        return self.sys_role_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    system_roles = models.ManyToManyField(SystemRole, related_name='users')

    class Meta:
        db_table = "tbl_user_profile"

    def __str__(self):
        return f"{self.user.username}'s Profile"