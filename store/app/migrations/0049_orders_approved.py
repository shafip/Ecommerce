# Generated by Django 4.2 on 2023-05-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_remove_orders_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]