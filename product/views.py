from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializations import *
from .models import * 
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
User = get_user_model()
# Create your views here.

# class ProductCategoryView(generics.ListAPIView):
#     queryset = ProductCategory.objects.all()
#    serializer_class = ProductCategorySerialization

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "role": user.role,
                    "email": email,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "success": "Login Successful",
                },
            )
        else:
            return Response({"error": "Wrong credentials"}, status=HTTP_401_UNAUTHORIZED)

class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Successfully logged out"})
        except Exception as e:
            return Response({"error": str(e)})
        
class ProductCategoryView(viewsets.ViewSet):
    def list(self, request):
       queryset = ProductCategory.objects.all()
       serializer = ProductCategorySerialization(queryset, many=True)
       return Response(serializer.data)

class ProductCategoryCreateView(generics.CreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerialization
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductCategoryGetbyidView(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryListSerialization
    lookup_field = 'id'

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization
    pagination_class = PageNumberPagination 
    permission_classes = [permissions.AllowAny]

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization
    permission_classes = [permissions.IsAuthenticated]

class ProductGetbyidView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization
    permission_classes = [permissions.IsAuthenticated]

#for the Contact US Serializer
class ContactGetView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactUsSerializer
    # permession = [permissions.IsAuthenticatedOrReadOnly]

class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactUsSerializer

class ContactDestroyView(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactUsSerializer