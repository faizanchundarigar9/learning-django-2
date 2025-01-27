from rest_framework.serializers import ModelSerializer
from home.models import Category, Product, Cart, Orders, OrderItems
from rest_framework import serializers

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','description','photo']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product        
        fields = '__all__'

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemsSerializer(ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'            

class LoginSerizlier(serializers.Serializer):
    email = serializers.CharField()        
    password = serializers.CharField()        
