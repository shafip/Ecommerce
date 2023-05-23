# Generated by Django 4.2 on 2023-05-12 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_product_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='session_key',
        ),
        migrations.AddField(
            model_name='orders',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
