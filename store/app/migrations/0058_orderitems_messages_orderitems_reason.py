# Generated by Django 4.2 on 2023-05-15 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_alter_orders_approved_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='messages',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='reason',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
