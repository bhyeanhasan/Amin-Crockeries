# Generated by Django 4.2.5 on 2023-09-23 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_order', '0010_alter_order_placed_at_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 17, 58, 13, 351396)),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 17, 58, 13, 352396)),
        ),
    ]
