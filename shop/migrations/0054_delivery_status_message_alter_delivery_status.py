# Generated by Django 4.1.1 on 2023-03-26 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0053_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='status_message',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(blank=True, choices=[('Cancelleed', 'Cancelled'), ('Delivered', 'Delivered'), ('Ready', 'Ready'), ('Postponed', 'Postponed'), ('Dispatched', 'Dispatched')], max_length=50, null=True),
        ),
    ]
