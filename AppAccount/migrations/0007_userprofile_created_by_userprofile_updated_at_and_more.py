# Generated by Django 5.1.1 on 2025-01-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAccount', '0006_alter_systemrole_sys_role_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]