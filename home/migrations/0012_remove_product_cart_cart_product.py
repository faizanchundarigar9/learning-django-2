# Generated by Django 5.1.3 on 2024-12-26 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_product_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
    ]
