# Generated by Django 4.2.5 on 2023-09-23 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_order', '0011_alter_order_placed_at_alter_review_review_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 18, 26, 43, 831671)),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 18, 26, 43, 832671)),
        ),
    ]
