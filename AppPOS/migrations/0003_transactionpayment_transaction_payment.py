# Generated by Django 5.1.1 on 2024-12-30 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppPOS', '0002_paymentmethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, null=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppPOS.paymentmethod')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppPOS.transaction')),
            ],
            options={
                'db_table': 'tbl_transaction_payment',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment',
            field=models.ManyToManyField(through='AppPOS.TransactionPayment', to='AppPOS.paymentmethod'),
        ),
    ]