# Generated by Django 4.2 on 2023-04-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_users_email_users_first_name_users_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
    ]
