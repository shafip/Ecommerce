# Generated by Django 4.2 on 2023-04-20 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_orderitems_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
