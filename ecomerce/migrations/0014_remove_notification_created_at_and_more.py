# Generated by Django 5.0.6 on 2024-09-08 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomerce', '0013_rename_is_viewed_notification_is_read_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='message',
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
