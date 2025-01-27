# Generated by Django 5.1.1 on 2025-01-21 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAdmin', '0002_rename_shopowner_shop_alter_shop_table'),
        ('AppProduct', '0002_outlet_address_outlet_contact_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.shop'),
        ),
        migrations.AlterUniqueTogether(
            name='outlet',
            unique_together={('shop', 'outlet_name')},
        ),
    ]
