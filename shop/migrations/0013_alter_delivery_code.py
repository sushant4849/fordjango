# Generated by Django 4.1.1 on 2023-03-21 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_delivery_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='code',
            field=models.IntegerField(blank=True, default=44176, null=True),
        ),
    ]