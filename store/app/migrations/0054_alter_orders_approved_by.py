# Generated by Django 4.2 on 2023-05-15 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_alter_orders_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='approved_by',
            field=models.BooleanField(choices=[('Return_approved', 'Return_approved'), ('Return_Rejected', 'Return_Rejected')], null=True),
        ),
    ]
