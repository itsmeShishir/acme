from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

#update Profile
class UpdateProfileSerializer(serializers.ModelSerializer):
    model = User
    fields = ('email', 'username',)

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()
        return instance


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


class ProductCategoryListSerialization(serializers.ModelSerializer):
   product = serializers.SerializerMethodField()
   class Meta:
       model = ProductCategory
       fields  = ['id', 'category_name', 'category_img','product']

   def get_product(self, obj):
        product = Product.objects.filter(category=obj)
        return ProductSerialization(product, many=True).data 
       

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerialization(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class EsewaPaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = esewaPayment
        fields = '__all__'