# Generated by Django 5.1.1 on 2025-01-23 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAdmin', '0002_rename_shopowner_shop_alter_shop_table'),
        ('AppProduct', '0005_brand_shop_alter_brand_brand_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributetype',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.shop'),
        ),
    ]