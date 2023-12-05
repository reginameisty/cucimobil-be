from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import Customer, Service, Order, Payment, Feedback, OrderHistory, Profile, Lapak, Chat, Message, User
from .serializers import CustomerSerializer, ServiceSerializer, OrderSerializer, PaymentSerializer, FeedbackSerializer, LapakSerializer, ProfileSerializer, ChatSerializer, MessageSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CustomerRegistrationForm
from django.contrib.auth.decorators import permission_required
from .utils import send_notification
from django.contrib.auth import authenticate, login
from .forms import OrderForm, LapakForm
import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth import authenticate, get_user_model, login
from .serializers import LoginSerializer
from django.contrib import admin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()

@api_view(['POST'])
def customer_registration(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        
        customer = Customer.objects.filter(email=username).first()

        if customer and customer.check_password(password):
            user = User.objects.get(username=customer.email)  
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

class LapakViewSet(viewsets.ModelViewSet):
    queryset = Lapak.objects.all()
    serializer_class = LapakSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(operation_description="Get list of lapaks with filtering and pagination")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'foto_profil': openapi.Schema(type=openapi.TYPE_FILE),
                'nama_lengkap': openapi.Schema(type=openapi.TYPE_STRING),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, enum=['Male', 'Female']),
                'tanggal_lahir': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            },
            required=['foto_profil', 'nama_lengkap', 'gender', 'tanggal_lahir'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Profile uploaded successfully',
                content={'application/json': {}},
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Bad Request',
                content={'application/json': {}},
            ),
        }
    )
    def post(self, request):
        return Response({'message': 'Profile uploaded successfully'})

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Profile download',
                content={'image/*': openapi.Schema(type=openapi.TYPE_FILE)},
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Profile not found',
                content={'application/json': {}},
            ),
        }
    )
    def get(self, request):
        return Response({'message': 'Profile download'})

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'nama_lengkap', 'gender', 'tanggal_lahir', 'alamat', 'lapak')
    list_filter = ('gender', 'lapak')

@login_required
def order_service(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.save()
        
            OrderHistory.objects.create(
                customer=order.customer,
                nomor_telepon=order.nomor_telepon,
                plat_nomor=order.plat_nomor,
                kategori_kendaraan=order.kategori_kendaraan,
                tanggal_cuci=order.tanggal_cuci,
                waktu_pengerjaan=order.waktu_pengerjaan,
                alamat=order.alamat,
            )
            return redirect('order_history')
        
    else:
        form = OrderForm()
        customers = Customer.objects.values('id', 'nama')

    context = {
        'form': form
    }
    return render(request, 'order_service.html', {'form': form, 'customers': customers})

@login_required
def order_history(request):
    order_history = OrderHistory.objects.all()
    context = {
        'order_history': order_history
    }

    return render(request, 'order_history.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')  
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def confirm_order(request, order_id):
    order = Order.objects.get(id=order_id)
    
    message = "Your order with ID {} has been confirmed.".format(order_id)
    send_notification(order.customer, message)

    return render(request, 'confirmation.html', {'order': order})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request):
    token = request.POST.get('stripeToken')

    try:
        charge = stripe.Charge.create(
            total=1000,  
            currency='Rp',  
            source=token 
        )

        return HttpResponse('Pembayaran berhasil')
    
    except stripe.error.CardError as e:
        error_msg = e.json_body.get('error', {}).get('message', '')
        return HttpResponse(f'Pembayaran gagal: {error_msg}')
    
def daftar_lapak(request):
    if request.method == 'POST':
        form = LapakForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('nama_url_yang_diinginkan')
    else:
        form = LapakForm()
    
    context = {'form': form}
    return render(request, 'nama_template.html', context)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

        else:
            return Response({'message': 'Login gagal. Cek kembali username dan password Anda.'}, status=status.HTTP_401_UNAUTHORIZED)
        
