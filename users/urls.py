from django.urls import path, include
from django.contrib.auth import urls
from .import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('user-add/',views.User_Add),
    path('user-view/<int:pk>/',views.User_View),
    path('user-update/<int:pk>/',views.User_Update),
    path('user-trust/<int:pk>/',views.Trust_View),
]