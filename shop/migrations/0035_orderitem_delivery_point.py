# Generated by Django 4.1.1 on 2023-03-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_remove_orderitem_min_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='delivery_point',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
