# Generated by Django 4.2 on 2023-05-15 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_alter_orders_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='approved_by',
            field=models.CharField(choices=[('confirmed', 'Confirmed'), ('placed', 'Placed'), ('shipped', 'Shipped'), ('cancel', 'cancel')], default='Return_request_accepted', max_length=20),
        ),
    ]
