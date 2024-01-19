# Generated by Django 4.1.4 on 2023-06-08 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_orders_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='Payment_status',
            field=models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'پرداخت انجام شده'), (3, 'پرداخت ناموفق'), (4, 'نامشخص'), (5, 'پرداخت با چک')], default=1, verbose_name='وضعیت پرداخت'),
        ),
    ]
