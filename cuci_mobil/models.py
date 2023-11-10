from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from drf_yasg.utils import swagger_auto_schema
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomerManager(BaseUserManager):
    def create_user(self, nama, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(nama=nama, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, email, password, **extra_fields)
    
    def create_customer(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

class Customer(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    nama = models.CharField(max_length=150)
    email = models.EmailField(default="")
   
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.nama 

  
class Service(models.Model):
    kategori = models.CharField(max_length=100)
    harga = models.IntegerField()

    def __str__(self):
        return self.kategori


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    nomor_telepon = models.CharField(    max_length=20, null=True)
    plat_nomor = models.CharField(max_length=50, null=True)
    kategori_kendaraan = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    tanggal_cuci = models.DateField(auto_now_add=True)
    waktu_pengerjaan = models.TimeField(auto_now_add=False, null=True)
    alamat = models.TextField(null=True)
    konfirmasi = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.customer} - {self.kategori_kendaraan}"


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tanggal_bayar = models.DateField()
    total = models.IntegerField()
    
    def __str__(self):
        return f"Payment by {self.customer} for {self.service} on {self.tanggal_bayar}"

class Feedback(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Feedback for Order {self.order}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    tanggal_order = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.customer.nama} - {self.service}"

    class Meta:
        verbose_name_plural = "Order History"

class Chat(models.Model):
    participants = models.ManyToManyField(Customer, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {', '.join([str(customer) for customer in self.participants.all()])}"

class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

@swagger_auto_schema()
class Lapak(models.Model):
    KATEGORI_CHOICES = (
        ('Cuci Mobil', 'Cuci Mobil'),
    )

    foto = models.ImageField(upload_to='lapak_photos/')
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    nama_lapak = models.CharField(max_length=200)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    harga = models.IntegerField()
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama_lapak
    
@swagger_auto_schema()
class Profile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    foto_profil = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    nama_lengkap = models.CharField(max_length=100)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tanggal_lahir = models.DateField()
    alamat = models.TextField(null=True, blank=True) 

    lapak = models.ForeignKey(Lapak, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama_lengkap