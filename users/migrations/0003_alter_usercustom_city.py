# Generated by Django 4.1.1 on 2023-03-25 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usercustom_delivery_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercustom',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]