# Generated by Django 4.1.2 on 2022-11-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_useraccount_city_useraccount_province_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='City',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='useraccount',
            old_name='Province',
            new_name='province',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='Description',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='Trust',
            field=models.BooleanField(default=False),
        ),
    ]
