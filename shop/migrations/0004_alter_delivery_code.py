# Generated by Django 4.1.1 on 2023-03-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_delivery_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='code',
            field=models.CharField(default=21862, max_length=5, null=True),
        ),
    ]
