# Generated by Django 5.0.6 on 2024-09-17 07:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce', '0016_supplier_products_stock_quantity_damagereport_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockpurchase',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='stockpurchase',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='stockpurchase',
            name='product',
        ),
        migrations.RemoveField(
            model_name='stockpurchase',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='stockpurchase',
            name='supplier',
        ),
        migrations.AddField(
            model_name='stockpurchase',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stockpurchase',
            name='purchase_number',
            field=models.CharField(default=0, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='stockpurchase',
            name='purchased_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockpurchase',
            name='total_purchase_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockpurchase',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OperationCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_type', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_costs', to='ecomerce.stockpurchase')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomerce.products')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ecomerce.stockpurchase')),
            ],
        ),
    ]
