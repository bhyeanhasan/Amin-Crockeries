# Generated by Django 4.2.5 on 2023-09-22 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0010_category_remove_wishlist_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
