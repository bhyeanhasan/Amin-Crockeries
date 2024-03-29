# Generated by Django 4.2.5 on 2023-09-24 16:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_user', '0016_alter_customer_registered_at'),
        ('manage_order', '0012_alter_order_placed_at_alter_review_review_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_user.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_user.customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='placed_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 22, 15, 4, 217567)),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Placed', max_length=500),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 22, 15, 4, 218578)),
        ),
    ]
