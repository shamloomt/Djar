from adminpanel.models import Product, Categories, Cart, Orders, Order_details, Base_Info, Pr_Fav
from rest_framework import serializers

class Product_Model_Serializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = '__all__'
  
class getcat_Serializer(serializers.ModelSerializer):
    category = serializers.CharField(source="Categories.name", read_only = True)
    
    class Meta:
        model = Categories
        fields = '__all__'

class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class Orders_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class Order_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order_details
        fields = '__all__'

class Base_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Base_Info
        fields = '__all__'

class Pr_Fav_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pr_Fav
        fields = '__all__'