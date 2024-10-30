from django.urls import path
from .views import *
urlpatterns = [
    #users
    path("register",RegisterUserView.as_view(), name="register"),
    path("login",LoginView.as_view(), name="login"),
    #category CRUD
    path("category",ProductCategoryView.as_view({'get': 'list'}), name="category"),
    path("create/category",ProductCategoryCreateView.as_view(), name="category"),
    path("getcategory/<int:id>",ProductCategoryGetbyidView.as_view(), name="category"),
    # Product list View
    path("product",ProductView.as_view(), name="product"),
    path("create/product",ProductCreateView.as_view(), name="product"),
    path("getproduct/<int:pk>",ProductGetbyidView.as_view(), name="product"),
    path("updateproduct/<int:pk>",ProductUpdateView.as_view(), name="product"),
    path("deleteproduct/<int:pk>",ProductDeleteView.as_view(), name="product"),

    # Contact us
    path("contactus",ContactGetView.as_view(), name="contactus"),
    path("create/contactus",ContactCreateView.as_view(), name="contactus"),
    path("delete/contactus/<int:id>",ContactDestroyView.as_view(), name="contactus"),

    #esewa
    path("esewa/callback",EsewaCallBackView.as_view(), name="esewa-callback"),
    path("esewa/payment",EsewaPaymentView.as_view(), name="esewa-Payment"),

    #lOGOUT
    path("logout",LogoutView.as_view(), name="logout"),

    #Seach Product
    path("search",SearchView.as_view(), name="search"),
]
