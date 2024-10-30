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
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Order
        fields = ['id','name', 'address', 'phone', 
                  'product', 'quantity', 'user', 'orderStatus', 'created_at']
        read_only_fields = ['orderStatus', 'created_at']
    
    def create (self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
    
    
class EsewaPaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), many=True)
    esewa_order_id = serializers.CharField(max_length=255)
    amount = serializers.IntegerField()

    class Meta:
        model = esewaPayment
        fields = ['id', 'esewa_order_id', 'amount', 'order_id', 'status', 'created_at']
        read_only_fields = ['status','created_at']

    # to validate the the data from esewa payment https://uat.esewa.com.np/epay/transrec   {
    def create(self, validated_data):
        payment = esewaPayment.objects.create(
            esewa_order_id=validated_data['esewa_order_id'],
            amount=validated_data['amount'],
            order=validated_data['order_id'],
            status = "Pending"
        )
        return payment
from rest_framework_simplejwt.tokens import RefreshToken
#LogOut
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()

        except Exception as e:
            self.fail('invalid_token')