# Generated by Django 4.2 on 2023-05-23 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0066_alter_varient_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='is_default',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]