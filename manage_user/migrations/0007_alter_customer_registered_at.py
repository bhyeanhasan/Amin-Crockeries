# Generated by Django 4.2.5 on 2023-09-22 21:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_user', '0006_rename_username_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='registered_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 9, 23, 3, 2, 42, 576271)),
        ),
    ]
