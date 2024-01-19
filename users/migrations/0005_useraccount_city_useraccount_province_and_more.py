# Generated by Django 4.1.2 on 2022-11-13 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_useraccount_frist_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='City',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='Province',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='address',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='mail',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='postcode',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
