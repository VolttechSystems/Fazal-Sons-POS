# Generated by Django 5.1.1 on 2025-01-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppProduct', '0003_outlet_shop_alter_outlet_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='outlet_code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='outlet',
            name='outlet_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]