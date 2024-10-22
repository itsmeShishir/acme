from django.urls import path
from .views import *
urlpatterns = [
    path("category",ProductCategoryView.as_view({'get': 'list'}), name="category"),
    path("create/category",ProductCategoryCreateView.as_view(), name="category"),
    path("product",ProductView.as_view(), name="product"),
    path("create/product",ProductCreateView.as_view(), name="product"),
    path("getproduct/<int:id>",ProductGetbyidView.as_view(), name="product"),
    path("updateproduct/<int:id>",ProductUpdateView.as_view(), name="product"),
    path("deleteproduct/<int:id>",ProductDeleteView.as_view(), name="product"),
]
