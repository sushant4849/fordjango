# Generated by Django 4.1.1 on 2023-03-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_alter_product_available_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('Ready', 'Ready'), ('Dispatched', 'Dispatched'), ('Delivered To Point', 'Delivered To Point'), ('Cancelled', 'Cancelled'), ('Postponed', 'Postponed')], default='Ready', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('Paid', 'Paid'), ('Not Paid', 'Not Paid')], default='Paid', max_length=50, null=True),
        ),
    ]
