# Generated by Django 4.2 on 2023-05-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_remove_orders_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='approved_by',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
