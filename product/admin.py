from django.contrib import admin
from .models import *
# Register your models here.
class ProductCategoryDetails(admin.ModelAdmin):
    list_display = ['id','category_name','category_img', 'created_at']
    search_fields = ['category_name']

class ProductDetails(admin.ModelAdmin):
    list_display = ['title', 'description', 'category', 'product_img',
    'stock','price', 'created_at']
    search_fields = ['title', 'stock']
    list_filter = ['created_at']

class ContactDetails(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone',
    'message', 'created_at']

admin.site.register(Contact, ContactDetails)
admin.site.register(ProductCategory, ProductCategoryDetails)
admin.site.register(Product, ProductDetails)
admin.site.register(CustomUsers)
admin.site.register(Order)
admin.site.register(esewaPayment)
admin.site.register(Cart)
