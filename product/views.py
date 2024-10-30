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

#for order
class OrderCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

from django.conf import settings

class EsewaPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        payment = esewaPayment.objects.create(
            esewa_order_id=order_id,
            amount=amount,
            order=order
        )

        payment_url = (
            f"{settings.ESEWA_PAYMENT_URL}?"
            f"amount={amount}&"
            f"pcd=0&psc=0&txnid=0&"
            f"tAmt={amount}&pid={payment.esewa_order_id}&"
            f"scd={settings.ESEWA_MERCHANT_ID}&"
            f"su={settings.ESEWA_SUCCESS_URL}&fn={settings.ESEWA_FAILED_URL}&"
        )

        return Response(payment_url)
    
class EsewaCallBackView(APIView):
    def post(self, request, *args, **kwargs):
        status_param = request.query_params.get('status')
        pid = request.query_params.get('oid')
        refId = request.query_params.get('refId')

        if status_param == 'success':
            try:
                payment = esewaPayment.objects.get(esewa_order_id=pid)
            except esewaPayment.DoesNotExist:
                return Response({'error': 'Payment not found'}, status=404)
            
            verification_url = (
                f"https://uat.esewa.com.np/epay/transrec?amt={payment.amount}&"
                f"scd={settings.ESEWA_MERCHANT_ID}"
                f"pid={payment.esewa_order_id}&rid={refId}"
            )
            
            response = request.post(verification_url)

            if response.status_code == 200:
                payment.status = "Success"
                payment.save()
                return Response({'success': 'Payment successful'}, status=200)
            else:
                payment.status = "Failed"
                payment.save()
                return Response({'error': 'Payment failed'}, status=400)

        else:
            return Response({'error': 'Payment failed'}, status=400)

# logout View
class LogoutView(APIView):
    def post(self, request):
        serializers = LogoutSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response({"success": "Successfully logged out"}, status=200)

#search product 
class SearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialization
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            search_query = self.request.query_params.get('title', None)

            if search_query:
                queryset = queryset.filter(title__icontains=search_query)

            return queryset
        except Exception as e:
            return Response({"error": "No Product Found"}, status=400)
       