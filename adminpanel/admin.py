from django.contrib import admin
from adminpanel.models import Product, Categories, Cart,Orders, Order_details, Base_Info, Pr_Fav, Discounts, Discounts_used

class Product_Mode(admin.ModelAdmin):
    list_display = ['id', 'name', 'cat_1']
    search_fields = ['name']

class Category_Mode(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']

class Cart_Mode(admin.ModelAdmin):
    list_display = ['id', 'User_ID', 'pr_ID']
    search_fields = ['User_ID']

class Orders_Mode(admin.ModelAdmin):
    list_display = ['order_id', 'User_ID', 'total_price', 'order_status', 'Payment_status']
    search_fields = ['order_id']

class OrderDT_Mode(admin.ModelAdmin):
    list_display = ['order_id', 'pr_ID']
    search_fields = ['order_id']

class BaseInfo_Mode(admin.ModelAdmin):
    list_display = ['caption', 'value']
    search_fields = ['caption']

class Pr_Fav_Mode(admin.ModelAdmin):
    list_display = ['User_ID', 'pr_ID']
    search_fields = ['User_ID']

class Discount_Mode(admin.ModelAdmin):
    list_display = ['code', 'code_type', 'discount', 'discount_type', 'usable', 'expire_date']
    search_fields = ['code']

class Discount_used_Mode(admin.ModelAdmin):
    list_display = ['discount_id', 'user_id', 'used']
    search_fields = ['user_id']

admin.site.register(Product, Product_Mode)
admin.site.register(Categories, Category_Mode)
admin.site.register(Cart, Cart_Mode)
admin.site.register(Orders, Orders_Mode)
admin.site.register(Order_details, OrderDT_Mode)
admin.site.register(Base_Info, BaseInfo_Mode)
admin.site.register(Pr_Fav, Pr_Fav_Mode)
admin.site.register(Discounts, Discount_Mode)
admin.site.register(Discounts_used, Discount_used_Mode)

