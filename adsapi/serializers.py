from rest_framework import serializers
from .models import  Product , WishListItems

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

 #Wishlist Serializers

class WishListItemsTestSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WishListItems
        fields = ['id','item']
        depth = 2       

  