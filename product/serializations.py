from rest_framework import serializers
from .models import *

class ProductCategorySerialization(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        # fields = "__all__"
        fields = ['id', 'category_name','category_img']
        
class ProductSerialization(serializers.ModelSerializer):
       class Meta:
        model = Product
        fields = ['id', 'title','description','product_img','stock',
        'price','category']