# Generated by Django 4.2 on 2023-05-16 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_orderitems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
