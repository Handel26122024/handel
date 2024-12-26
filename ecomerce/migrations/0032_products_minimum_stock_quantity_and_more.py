# Generated by Django 5.0.6 on 2024-12-16 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce', '0031_locationupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='minimum_stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
