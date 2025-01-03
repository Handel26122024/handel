# Generated by Django 5.0.6 on 2024-11-11 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce', '0028_rename_amount_paid_order_total_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='order',
            name='change',
        ),
        migrations.AddField(
            model_name='paymentproof',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='paymentproof',
            name='change',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
