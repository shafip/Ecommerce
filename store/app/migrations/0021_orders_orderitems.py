# Generated by Django 4.2 on 2023-04-18 08:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=10, null=True, unique=True)),
                ('items', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('shipping', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.shipping')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orders')),
                ('varient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.varient')),
            ],
        ),
    ]