# Generated by Django 4.1.1 on 2023-04-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0056_cart_text_1_cart_text_2_cart_text_3_cart_text_4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
