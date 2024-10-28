from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Permission, Group
from core import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class CustomUsers(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.IntegerField(default=1) #0-> admin , #1-> user normal one 
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='charging_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='charging_user_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=255)  
    category_img = models.ImageField(upload_to="category/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.category_name} and {self.created_at}"
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()   
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    product_img = models.ImageField(upload_to="product/", null=True, blank=True)
    stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    shipping_cost = models.IntegerField(default=0)
    is_shipping = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.title} and {self.category}"

class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    address = models.CharField(max_length=255)
    phone = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, null=True, blank=True)   
    orderStatus = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    
class esewaPayment(models.Model):
    esewa_order_id = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=[
        ('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], 
        default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.esewa_order_id

class Cart(models.Model):
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title