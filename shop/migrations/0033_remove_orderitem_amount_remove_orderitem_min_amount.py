# Generated by Django 4.1.1 on 2023-03-23 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_remove_delivery_code_delivery_sales_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='min_amount',
        ),
    ]