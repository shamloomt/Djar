# Generated by Django 4.1.2 on 2023-05-23 06:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Base_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='عنوان')),
                ('value', models.CharField(max_length=150, verbose_name='مقدار')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='عنوان')),
                ('parent', models.IntegerField(default=0, help_text='برای دسته های مادر عدد صفر و برای دسته های فرزند، عدد مربوط به دسته ی مادر را وارد کنید', verbose_name='دسته ی مادر')),
                ('pic_cat', models.ImageField(blank=True, default='store_image/cats/djar.png', null=True, upload_to='store_image/cats/', verbose_name='تصویر دسته بندی')),
            ],
            options={
                'verbose_name': 'دسته بندی محصولات',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True, default=0, unique=True, verbose_name='شماره سفارش')),
                ('User_ID', models.IntegerField(blank=True, default=0, verbose_name='آی دی کاربر')),
                ('total_price', models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True, verbose_name='مجموع قیمت')),
                ('order_status', models.IntegerField(choices=[(1, 'سفارش جدید'), (2, 'تایید سفارش'), (3, 'رد سفارش')], default=1, verbose_name='وضعیت')),
                ('Payment_status', models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'پرداخت انجام شده'), (3, 'پرداخت ناموفق'), (4, 'نامشخص')], default=1, verbose_name='وضعیت پرداخت')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='زمان ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
            ],
            options={
                'verbose_name': 'سفارشات',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='عنوان محصول')),
                ('barcode', models.CharField(blank=True, max_length=15, verbose_name='بارکد')),
                ('stock', models.IntegerField(blank=True, help_text='اگر موجوی محصول شما نامحدود است این فیلد را خالی بگذارید', null=True, verbose_name='وضعیت موجودی')),
                ('sold', models.IntegerField(blank=True, null=True, verbose_name='فروخته شده')),
                ('des_short', models.CharField(blank=True, max_length=40, null=True, verbose_name='توضیحات کوتاه')),
                ('des_long', models.CharField(blank=True, max_length=100, null=True, verbose_name='توضیحات تکمیلی')),
                ('image_1', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 1 (تصویر اصلی)')),
                ('image_2', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 2')),
                ('image_3', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 3')),
                ('image_4', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 4')),
                ('image_5', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 5')),
                ('image_6', models.ImageField(blank=True, default='', null=True, upload_to='store_image/', verbose_name='تصویر 6')),
                ('single_pack_WS', models.BooleanField(default=False, verbose_name='تکی (عمده)')),
                ('single_price_WS', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('single_priceOff_WS', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد با تخفیف')),
                ('packet_pack_WS', models.BooleanField(default=False, verbose_name='بسته (عمده)')),
                ('packet_Qty_WS', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد محصول در هر بسته')),
                ('packet_price_WS_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('packet_price_WS_box', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر بسته')),
                ('packet_priceOff_WS', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر بسته با تخفیف')),
                ('box_pack_WS', models.BooleanField(default=False, verbose_name='جعبه (عمده)')),
                ('box_Qty_WS', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد محصول در هر جعبه')),
                ('box_price_WS_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('box_price_WS_box', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر جعبه')),
                ('box_priceOff_WS', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر جعبه با تخفیف')),
                ('single_pack_RE', models.BooleanField(default=False, verbose_name='تکی (خرده)')),
                ('single_price_RE', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('single_priceOff_RE', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد با تخفیف')),
                ('packet_pack_RE', models.BooleanField(default=False, verbose_name='بسته (خرده)')),
                ('packet_Qty_RE', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد محصول در هر بسته')),
                ('packet_price_RE_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('packet_price_RE_packet', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر بسته')),
                ('packet_priceOff_RE', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر بسته با تخفیف')),
                ('box_pack_RE', models.BooleanField(default=False, verbose_name='جعبه (خرده)')),
                ('box_Qty_RE', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد محصول در هر جعبه')),
                ('box_price_RE_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('box_price_RE_box', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر جعبه')),
                ('box_priceOff_RE', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر جعبه با تخفیف')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='زمان ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('cat_1', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cat_1', to='adminpanel.categories', verbose_name='دسته بندی 1 (دسته بندی اصلی)')),
                ('cat_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cat_2', to='adminpanel.categories', verbose_name='دسته بندی 2')),
                ('cat_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cat_3', to='adminpanel.categories', verbose_name='دسته بندی 3')),
                ('cat_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cat_4', to='adminpanel.categories', verbose_name='دسته بندی 4')),
                ('cat_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cat_5', to='adminpanel.categories', verbose_name='دسته بندی 5')),
            ],
            options={
                'verbose_name': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Pr_Fav',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_ID', models.IntegerField(blank=True, default=0, verbose_name='آی دی کاربر')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='زمان ایجاد')),
                ('pr_ID', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ProId_Fav', to='adminpanel.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'محصولات مورد علاقه کاربران',
            },
        ),
        migrations.CreateModel(
            name='Order_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_type', models.IntegerField(blank=True, choices=[(1, 'عمده'), (2, 'خرده')], verbose_name='نوع فروش')),
                ('single_pack', models.BooleanField(default=False, verbose_name='تکی')),
                ('single_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('Qty_select_single', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش تکی')),
                ('packet_pack', models.BooleanField(default=False, verbose_name='بسته')),
                ('Qty_in_packet', models.IntegerField(blank=True, default=0, verbose_name='تعداد محصول در هر بسته')),
                ('packet_price_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر محصول در بسته')),
                ('Qty_select_packet', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش بتسه ای')),
                ('box_pack', models.BooleanField(default=False, verbose_name='جعبه')),
                ('Qty_in_box', models.IntegerField(blank=True, default=0, verbose_name='تعداد محصول در هر جعبه')),
                ('box_price_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر محصول در جعبه')),
                ('Qty_select_box', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش جعبه ای')),
                ('Qty_all_Select', models.IntegerField(blank=True, default=0, verbose_name='تعداد کل')),
                ('total_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='مجموع قیمت')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='زمان ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('order_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rel_orderid', to='adminpanel.orders', to_field='order_id', verbose_name='شماره سفارش')),
                ('pr_ID', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ProId_orderDT', to='adminpanel.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'جزئیات سفارش',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_ID', models.IntegerField(blank=True, default=0)),
                ('sale_type', models.IntegerField(blank=True, choices=[(0, 'نامشخص'), (1, 'عمده'), (2, 'خرده')], default=0, verbose_name='نوع فروش')),
                ('single_pack', models.BooleanField(default=False, verbose_name='تکی')),
                ('single_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر عدد')),
                ('Qty_select_single', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش تکی')),
                ('packet_pack', models.BooleanField(default=False, verbose_name='بسته')),
                ('Qty_in_packet', models.IntegerField(blank=True, default=0, verbose_name='تعداد محصول در هر بسته')),
                ('packet_price_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر محصول در بسته')),
                ('Qty_select_packet', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش بتسه ای')),
                ('box_pack', models.BooleanField(default=False, verbose_name='جعبه')),
                ('Qty_in_box', models.IntegerField(blank=True, default=0, verbose_name='تعداد محصول در هر جعبه')),
                ('box_price_one', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='قیمت هر محصول در جعبه')),
                ('Qty_select_box', models.IntegerField(blank=True, default=0, verbose_name='تعداد سفارش جعبه ای')),
                ('Qty_all_Select', models.IntegerField(blank=True, default=0, verbose_name='تعداد کل')),
                ('total_price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='مجموع قیمت')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pr_ID', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ProId_cart', to='adminpanel.product', verbose_name='عنوان محصول')),
            ],
            options={
                'verbose_name': 'سبد خرید کاربران',
            },
        ),
    ]
