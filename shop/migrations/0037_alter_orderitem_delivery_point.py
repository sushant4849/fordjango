# Generated by Django 4.1.1 on 2023-03-23 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_alter_orderitem_delivery_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='delivery_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.deliverypoint'),
        ),
    ]
