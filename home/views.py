from django.shortcuts import render
from adminpanel.models import Categories

def product_categorie(request):
    data = Categories.objects.all()
    p_name = { 'Category' : data }
    return render (request , 'home.html', p_name)

def product(request, postid):
    data = Categories.objects.all()
    p_name = { 'postid' : postid , 'Category' : data }
    return render (request , 'product.html', p_name)