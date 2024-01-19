from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from datetime import datetime

class UserAccountMnager(BaseUserManager):
    def create_user(self, username, password = None):

        if not username:
            raise ValueError('user must have an username')

        else:
            user = self.model(username = username)
            user.set_password(password)
            user.is_active = True
            # user.set_unusable_password()
            user.save()

            return user

    def create_superuser(self, username, password):
        
        user = self.create_user(username = username, password= password)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser):
    
    user_pic = models.ImageField(default = '', upload_to = 'store_image/users_pic/', null = True, blank = True, verbose_name='تصویر کاربر')
    username = models.IntegerField(unique=True, verbose_name='شماره موبایل (نام کاربری)') #phone number
    frist_name = models.CharField(max_length=50, null = True, blank = True, default = '', verbose_name='نام')
    last_name = models.CharField(max_length=50, null = True, blank = True, default = '', verbose_name='نام خانوادگی')
    province  = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='استان')
    city = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='شهر')
    address = models.CharField(max_length=100, null = True, blank = True, default = '', verbose_name='آدرس')
    phone = models.IntegerField(null = True, blank = True, default = 0, verbose_name = 'شماره تلفن ثابت')
    postcode = models.IntegerField(null = True, blank = True, default = 0, verbose_name='کد پستی')
    mail = models.CharField(max_length=30, null = True, blank = True, default = '', verbose_name='ایمیل')
    Description = models.CharField(max_length=200, null = True, blank = True, default = '', verbose_name='توضیحات')

    Trust = models.BooleanField(default = False, verbose_name='مورد اعتماد') # برای خرید اقساطی و چک

    is_active = models.BooleanField(default=True, verbose_name='وضعیت فعال بودن حساب') #account enable/disable
    is_staff = models.BooleanField(default=False, verbose_name='مدیر کل بودن') #super user

    created_at = models.DateTimeField(default = datetime.now, verbose_name = 'زمان ایجاد')
    updated = models.DateTimeField(auto_now = True, verbose_name = 'اخرین بروزرسانی')

    objects = UserAccountMnager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return str(self.username)


    class Meta:
        verbose_name = 'کاربران'


class Trust(models.Model):
    User_ID = models.ForeignKey(UserAccount, on_delete = models.CASCADE, related_name='rel_userId', null = False, default = 0, verbose_name='آی کاربر')

    class Meta:
        verbose_name = 'کاربران مورد اعتماد'