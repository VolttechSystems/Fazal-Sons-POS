# Generated by Django 5.1.1 on 2025-01-20 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('no_of_outlets', models.IntegerField(null=True)),
                ('no_of_registered_outlets', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'tbl_shop_owner',
            },
        ),
    ]
