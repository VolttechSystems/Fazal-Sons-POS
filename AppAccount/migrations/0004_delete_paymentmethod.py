# Generated by Django 5.1.1 on 2024-12-30 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppAccount', '0003_paymentmethod'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
    ]