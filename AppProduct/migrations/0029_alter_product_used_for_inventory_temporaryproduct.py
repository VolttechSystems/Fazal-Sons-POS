# Generated by Django 5.1.1 on 2024-10-22 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppProduct', '0028_alter_outlet_outlet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='used_for_inventory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='TemporaryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('season', models.CharField(choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn'), ('Winter', 'Winter')], default='Spring', max_length=10)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='Product')),
                ('used_for_inventory', models.CharField(blank=True, max_length=100, null=True)),
                ('cost_price', models.CharField(blank=True, max_length=100, null=True)),
                ('selling_price', models.CharField(blank=True, max_length=100, null=True)),
                ('discount_price', models.CharField(blank=True, max_length=100, null=True)),
                ('wholesale_price', models.CharField(blank=True, max_length=100, null=True)),
                ('retail_price', models.CharField(blank=True, max_length=100, null=True)),
                ('token_price', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('created_by', models.CharField(blank=True, max_length=200, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(blank=True, max_length=200, null=True)),
                ('brand_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppProduct.brand', to_field='brand_name')),
                ('outlet_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppProduct.outlet', to_field='outlet_name')),
                ('sub_category_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppProduct.subcategory', to_field='sub_category_name')),
            ],
            options={
                'db_table': 'tbl_product_temp',
            },
        ),
    ]