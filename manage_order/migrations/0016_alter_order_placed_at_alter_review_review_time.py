# Generated by Django 5.0.4 on 2024-04-26 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_order', '0015_alter_order_placed_at_alter_review_review_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 26, 12, 0, 17, 396379)),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 26, 12, 0, 17, 396379)),
        ),
    ]
