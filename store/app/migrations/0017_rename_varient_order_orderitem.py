# Generated by Django 4.2 on 2023-04-17 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_orderitem_varient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='varient',
            new_name='orderitem',
        ),
    ]
