from django.db import models
from datetime import datetime
# from django_jalali import models as jmodel
# import jdatetime
# from jalali_date import datetime2jalali, date2jalali

class Categories(models.Model):
    name = models.CharField(max_length = 30, blank = False, verbose_name='عنوان')
    parent = models.IntegerField(default= 0, help_text = 'برای دسته های مادر عدد صفر و برای دسته های فرزند، عدد مربوط به دسته ی مادر را وارد کنید', verbose_name = 'دسته ی مادر')
    pic_cat = models.ImageField(upload_to = 'store_image/cats/',default = 'store_image/cats/djar.png', null = True, blank = True, verbose_name='تصویر دسته بندی')

    class Meta:
        verbose_name = 'دسته بندی محصولات'

    def __str__(self):
        if self.parent == 0:
            return " + " + self.name
        else:
            return " - " + self.name
        
class Product(models.Model):
    
    name = models.CharField(max_length = 30, blank = False, verbose_name='عنوان محصول')
    
    barcode = models.CharField(max_length = 15, null = False, blank = True, verbose_name='بارکد')
    stock = models.IntegerField(null = True, blank = True, verbose_name='وضعیت موجودی', help_text='اگر موجوی محصول شما نامحدود است این فیلد را خالی بگذارید') # موجودی کلی محصول
    sold = models.IntegerField(null = True, blank = True, verbose_name='فروخته شده') # تعداد محصول فروخته شده

    des_short = models.CharField(max_length = 40, null = True, blank = True, verbose_name='توضیحات کوتاه')
    des_long = models.CharField(max_length = 250, null = True, blank = True, verbose_name='توضیحات تکمیلی')

    image_1 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 1 (تصویر اصلی)')
    image_2 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 2')
    image_3 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 3')
    image_4 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 4')
    image_5 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 5')
    image_6 = models.ImageField(default = '', upload_to = 'store_image/', null = True, blank = True, verbose_name='تصویر 6')

    cat_1 = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name='rel_cat_1', null = True, blank = True, default = 1, verbose_name='دسته بندی 1 (دسته بندی اصلی)')
    cat_2 = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name='rel_cat_2', null = True, blank = True, verbose_name='دسته بندی 2')
    cat_3 = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name='rel_cat_3', null = True, blank = True, verbose_name='دسته بندی 3')
    cat_4 = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name='rel_cat_4', null = True, blank = True, verbose_name='دسته بندی 4')
    cat_5 = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name='rel_cat_5', null = True, blank = True, verbose_name='دسته بندی 5')
    
    ##### عمده فروشی ####    
    single_pack_WS = models.BooleanField(default=False, verbose_name='تکی (عمده)')
    # single_Qty_WS = models.IntegerField(null = True, blank = True, default = 0, verbose_name='')
    single_price_WS = models.DecimalField(max_digits = 9, decimal_places = 0 , null = True, blank = True, verbose_name='قیمت هر عدد')
    single_priceOff_WS = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد با تخفیف')

    packet_pack_WS = models.BooleanField(default=False, verbose_name='بسته (عمده)')
    packet_Qty_WS = models.IntegerField(null = True, blank = True, default = 0, verbose_name='تعداد محصول در هر بسته')
    packet_price_WS_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    packet_price_WS_box = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر بسته')
    packet_priceOff_WS = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر بسته با تخفیف')

    box_pack_WS = models.BooleanField(default=False, verbose_name='جعبه (عمده)')
    box_Qty_WS = models.IntegerField(null = True, blank = True, default = 0, verbose_name='تعداد محصول در هر جعبه')
    box_price_WS_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    box_price_WS_box = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر جعبه')
    box_priceOff_WS = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر جعبه با تخفیف')

    ##### خرده فروشی ####
    single_pack_RE = models.BooleanField(default=False, verbose_name='تکی (خرده)')
    # single_Qty_RE = models.IntegerField(null = True, blank = True, default = 0, verbose_name='')
    single_price_RE = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    single_priceOff_RE = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد با تخفیف')
    
    packet_pack_RE = models.BooleanField(default=False, verbose_name='بسته (خرده)')
    packet_Qty_RE = models.IntegerField(null = True, blank = True, default = 0, verbose_name='تعداد محصول در هر بسته')
    packet_price_RE_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    packet_price_RE_packet = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر بسته')
    packet_priceOff_RE = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر بسته با تخفیف')
    
    box_pack_RE = models.BooleanField(default=False, verbose_name='جعبه (خرده)')
    box_Qty_RE = models.IntegerField(null = True, blank = True, default = 0, verbose_name='تعداد محصول در هر جعبه')
    box_price_RE_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    box_price_RE_box = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر جعبه')
    box_priceOff_RE = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر جعبه با تخفیف')
    
    created_at = models.DateTimeField(default = datetime.now, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now = True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصولات'

class Cart(models.Model):
    
    RE_OR_WS = (
        (0, 'نامشخص'),
        (1, 'عمده'),
        (2, 'خرده')
    )

    User_ID = models.IntegerField(null = False, blank = True, default=0)
    pr_ID = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='rel_ProId_cart', null = False, default=0, verbose_name='عنوان محصول')
   
    sale_type = models.IntegerField(choices = RE_OR_WS, blank = True,default=0, verbose_name = 'نوع فروش')

    single_pack = models.BooleanField(default=False, verbose_name='تکی')
    single_price = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    Qty_select_single = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش تکی')

    packet_pack = models.BooleanField(default=False, verbose_name='بسته')
    Qty_in_packet = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد محصول در هر بسته')
    packet_price_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر محصول در بسته')
    Qty_select_packet = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش بتسه ای')

    box_pack = models.BooleanField(default=False, verbose_name='جعبه')
    Qty_in_box = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد محصول در هر جعبه')
    box_price_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر محصول در جعبه')
    Qty_select_box = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش جعبه ای')

    Qty_all_Select = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد کل')

    total_price = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name = 'مجموع قیمت')

    created_at = models.DateTimeField(default = datetime.now)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = 'سبد خرید کاربران'

class Orders(models.Model):

    status_ord = (
        (1, 'سفارش جدید'),
        (2, 'تایید سفارش'),
        (3, 'رد سفارش'),
    )

    status_pay = (
        (1, 'در انتظار پرداخت'),
        (2, 'پرداخت انجام شده'),
        (3, 'پرداخت ناموفق'),
        (4, 'نامشخص'),
        (5, 'پرداخت با چک')
    )

    order_id = models.IntegerField(unique=True, null = False, blank = True, default = 0, verbose_name='شماره سفارش')
    User_ID = models.IntegerField(null = False, blank = True, default = 0, verbose_name='آی دی کاربر')
    
    total_price = models.DecimalField(max_digits = 12, decimal_places = 0, null = True, blank = True, verbose_name = 'مجموع قیمت')
    discount_code = models.CharField(max_length=50, verbose_name='کد تخفیف')
    payable = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name = 'مبلغ قابل پرداخت')
    
    order_status = models.IntegerField(choices = status_ord, default = 1, verbose_name='وضعیت')
    Payment_status = models.IntegerField(choices = status_pay, default = 1, verbose_name='وضعیت پرداخت')

    frist_name = models.CharField(max_length=50, null = True, blank = True, default = '', verbose_name='نام گیرنده')
    last_name = models.CharField(max_length=50, null = True, blank = True, default = '', verbose_name='نام خانوادگی گیرنده')
    province  = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='استان')
    city = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='شهر')
    address = models.CharField(max_length=100, null = True, blank = True, default = '', verbose_name='آدرس')
    mobile = models.IntegerField(null = True, blank = True, default = 0, verbose_name = 'شماره موبایل')
    phone = models.IntegerField(null = True, blank = True, default = 0, verbose_name = 'شماره تلفن ثابت')
    postcode = models.IntegerField(null = True, blank = True, default = 0, verbose_name='کد پستی')
    mail = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='ایمیل')
    Description = models.CharField(max_length=200, null = True, blank = True, default = '', verbose_name='توضیحات')

    created_at = models.DateTimeField(default = datetime.now, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now = True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'سفارشات'

    def __str__(self):
        return str(self.order_id)

class Order_details(models.Model):

    RE_OR_WS = (
        (1, 'عمده'),
        (2, 'خرده')
    )

    order_id = models.ForeignKey(Orders, to_field='order_id', on_delete = models.CASCADE, related_name='rel_orderid', null = False, default = 0, verbose_name='شماره سفارش')

    pr_ID = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='rel_ProId_orderDT', null = False, default = 0, verbose_name='محصول')

    sale_type = models.IntegerField(choices = RE_OR_WS, blank = True, verbose_name = 'نوع فروش')
   
    single_pack = models.BooleanField(default=False, verbose_name='تکی')
    single_price = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر عدد')
    Qty_select_single = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش تکی')

    packet_pack = models.BooleanField(default=False, verbose_name='بسته')
    Qty_in_packet = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد محصول در هر بسته')
    packet_price_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر محصول در بسته')
    Qty_select_packet = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش بتسه ای')

    box_pack = models.BooleanField(default=False, verbose_name='جعبه')
    Qty_in_box = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد محصول در هر جعبه')
    box_price_one = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name='قیمت هر محصول در جعبه')
    Qty_select_box = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد سفارش جعبه ای')

    Qty_all_Select = models.IntegerField(null = False, blank = True, default=0, verbose_name = 'تعداد کل')

    total_price = models.DecimalField(max_digits = 9, decimal_places = 0, null = True, blank = True, verbose_name = 'مجموع قیمت')

    created_at = models.DateTimeField(default = datetime.now, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now = True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'جزئیات سفارش'

class Base_Info(models.Model):
    caption = models.CharField(max_length=50, verbose_name='عنوان')
    value = models.CharField(max_length=150, verbose_name='مقدار')
    
class Pr_Fav(models.Model):
    User_ID = models.IntegerField(null = False, blank = True, default = 0, verbose_name='آی دی کاربر')
    pr_ID = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='rel_ProId_Fav', null = False, default = 0, verbose_name='محصول')

    created_at = models.DateTimeField(default = datetime.now, verbose_name='زمان ایجاد')

    class Meta:
        verbose_name = 'محصولات مورد علاقه کاربران'

class Discounts(models.Model):
    C_type = (
        (1, 'عمومی'),
        (2, 'خصوصی')
    )

    D_type = (
        (1, 'درصد'),
        (2, 'تومان')
    )

    code = models.CharField(max_length=50, verbose_name='کد تخفیف', unique=True)

    code_type = models.IntegerField(choices = C_type, blank = True, verbose_name = 'نوع کد')
    discount = models.IntegerField(null = False, blank = False, verbose_name='مقدار تخفیف')
    discount_type = models.IntegerField(choices = D_type, blank = True, verbose_name = 'نوع تخفیف')
    
    usable = models.IntegerField(null = False, blank = False, verbose_name='تعداد دفعات قابل استفاده برای هر کاربر')
    expire_date = models.DateField (blank=True, null=True)

    class Meta:
        verbose_name = 'کد تخفیف'

class Discounts_used(models.Model):
    discount_id = models.ForeignKey(Discounts, to_field='code', on_delete = models.CASCADE, related_name='rel_disCode', null = False, verbose_name='کد تخفیف')
    user_id = models.IntegerField(null = False, blank = True, default = 0, verbose_name = 'آی دی کاربر')
    used = models.IntegerField(null = False, blank = False, verbose_name = 'تعداد دفعات استفاده شده')
    
    class Meta:
        verbose_name = 'کد تخفیف های استفاده شده'