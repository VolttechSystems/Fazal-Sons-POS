# Generated by Django 5.1.1 on 2025-01-23 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAdmin', '0002_rename_shopowner_shop_alter_shop_table'),
        ('AppStock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.shop'),
        ),
    ]
