# Generated by Django 4.1.2 on 2022-11-13 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_city_useraccount_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
