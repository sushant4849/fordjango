# Generated by Django 4.1.1 on 2023-05-12 16:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_usercustom_pin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercustom",
            name="pin",
            field=models.PositiveIntegerField(
                blank=True,
                default=6622,
                null=True,
                validators=[django.core.validators.MaxValueValidator(9999)],
            ),
        ),
    ]
