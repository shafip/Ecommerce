# Generated by Django 4.2 on 2023-05-18 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0064_varient_banner_varient_image_varient_image2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='banner',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image3',
        ),
    ]
