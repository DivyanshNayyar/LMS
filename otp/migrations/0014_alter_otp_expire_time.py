# Generated by Django 3.2.5 on 2021-11-05 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0013_auto_20211105_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='Expire_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 23, 57, 46, 431045)),
        ),
    ]
