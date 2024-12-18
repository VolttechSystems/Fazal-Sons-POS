from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SystemRole(models.Model):
    sys_role_code = models.CharField(max_length=200, null=True, unique=True)  # SYSR-1
    sys_role_name = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True,  blank=True)

    class Meta:
        db_table = 'tbl_system_role'

    def __str__(self):
        return self.sys_role_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    system_roles = models.ManyToManyField(
        'SystemRole',
        related_name='users'
    )
    class Meta:
        db_table = 'tbl_user_profile'

    def __str__(self):

        return f"{self.user.username}'s Profile"