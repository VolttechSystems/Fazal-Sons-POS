# Generated by Django 5.1.1 on 2024-11-04 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppPOS', '0003_alter_feerecord_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='feerecord',
            table='tbl_transaction_additional_fee',
        ),
    ]