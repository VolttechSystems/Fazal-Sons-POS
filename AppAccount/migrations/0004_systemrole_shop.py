# Generated by Django 5.1.1 on 2025-01-22 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAccount', '0003_userprofile_shop'),
        ('AppAdmin', '0002_rename_shopowner_shop_alter_shop_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemrole',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.shop'),
        ),
    ]
