# Generated by Django 4.2 on 2023-05-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_orderitems_messages_orderitems_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='status',
            field=models.CharField(blank=True, default='confirmed', max_length=20, null=True),
        ),
    ]