# Generated by Django 5.1.1 on 2024-11-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppPOS', '0009_salesman_outlet_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesman',
            name='status',
            field=models.CharField(blank=True, null=True),
        ),
    ]