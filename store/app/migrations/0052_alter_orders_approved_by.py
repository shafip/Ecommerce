# Generated by Django 4.2 on 2023-05-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_orders_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='approved_by',
            field=models.BooleanField(choices=[('cancel_approved', 'cancel_approved'), ('cancel_declined', 'cancel_declined')], default=False, null=True),
        ),
    ]
