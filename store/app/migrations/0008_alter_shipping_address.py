# Generated by Django 4.2 on 2023-04-14 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_users_groups_users_is_staff_users_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='address',
            field=models.CharField(default='', max_length=50),
        ),
    ]
