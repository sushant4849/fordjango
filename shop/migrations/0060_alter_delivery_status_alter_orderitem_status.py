# Generated by Django 4.1.1 on 2023-05-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0059_product_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Cancelled", "Cancelled"),
                    ("Delivered", "Delivered"),
                    ("Ready", "Ready"),
                    ("Postponed", "Postponed"),
                    ("Dispatched", "Dispatched"),
                ],
                default="Ready",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="status",
            field=models.CharField(
                choices=[
                    ("Cancelled", "Cancelled"),
                    ("Done", "Done"),
                    ("Pending", "Pending"),
                ],
                default="Pending",
                max_length=20,
                null=True,
            ),
        ),
    ]
