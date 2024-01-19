from django.urls import path
from .views import product_categorie, product 

urlpatterns = [
    path('', product_categorie, name="home"),
    path('<postid>', product, name='product' ),
]