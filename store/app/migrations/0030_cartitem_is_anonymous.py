# Generated by Django 4.2 on 2023-04-24 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_remove_shipping_email_shipping_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
