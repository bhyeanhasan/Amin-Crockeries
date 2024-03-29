# Generated by Django 4.2.5 on 2023-09-22 20:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manage_product', '0010_category_remove_wishlist_customer_and_more'),
        ('manage_user', '0004_address_customer_delete_profile_address_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField(default=0.0)),
                ('placed_at', models.DateTimeField(default=datetime.datetime(2023, 9, 23, 2, 14, 38, 272303))),
                ('status', models.CharField(max_length=500)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_user.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_user.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_product.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_user.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_user.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_product.product')),
            ],
        ),
    ]
