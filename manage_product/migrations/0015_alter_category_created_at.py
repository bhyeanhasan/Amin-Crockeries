# Generated by Django 4.2.5 on 2023-09-23 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0014_alter_category_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 23, 18, 26, 43, 829672)),
        ),
    ]
