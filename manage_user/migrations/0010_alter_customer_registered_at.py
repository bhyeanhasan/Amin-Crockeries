# Generated by Django 4.2.5 on 2023-09-22 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_user', '0009_alter_customer_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 3, 33, 19, 575580)),
        ),
    ]
