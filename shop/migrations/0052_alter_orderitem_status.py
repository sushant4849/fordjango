# Generated by Django 4.1.1 on 2023-03-25 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0051_remove_orderitem_delivery_point_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending')], default='Done', max_length=20, null=True),
        ),
    ]