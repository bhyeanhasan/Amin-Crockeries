# Generated by Django 5.0.4 on 2024-04-26 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0016_alter_category_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 26, 11, 52, 34, 98065)),
        ),
    ]
