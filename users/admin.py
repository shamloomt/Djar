from django.contrib import admin
from .models import UserAccount, Trust


class User_Mode(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_active', 'is_staff']
    search_fields = ['username']

admin.site.register(UserAccount, User_Mode)

class User_Trust(admin.ModelAdmin):
    list_display = ['id', 'User_ID']
    search_fields = ['User_ID']

admin.site.register(Trust, User_Trust)