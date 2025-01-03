# Generated by Django 5.0.6 on 2024-11-12 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_businessprofile_business_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesslocation',
            name='location_type',
            field=models.CharField(choices=[('Delivery Point', 'Delivery Point'), ('Pickup Point', 'Pickup Point')], default='Delivery Point', max_length=50),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='businesslocation',
            name='staff_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_locations', to='business.businessstaff'),
        ),
    ]
