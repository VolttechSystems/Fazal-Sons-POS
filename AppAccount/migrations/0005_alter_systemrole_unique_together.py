# Generated by Django 5.1.1 on 2025-01-22 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppAccount', '0004_systemrole_shop'),
        ('AppAdmin', '0002_rename_shopowner_shop_alter_shop_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='systemrole',
            unique_together={('shop', 'sys_role_name')},
        ),
    ]