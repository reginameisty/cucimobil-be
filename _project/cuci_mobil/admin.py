from django.contrib import admin
from .models import Customer, Service, Order, Payment, Feedback, Lapak, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.db import models

@admin.register(Customer)
class CustomCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'email')  

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'kategori', 'harga')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'nomor_telepon', 'plat_nomor', 'kategori_kendaraan', 'tanggal_cuci', 'waktu_pengerjaan', 'alamat', 'konfirmasi')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'service', 'tanggal_bayar', 'total')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'rating', 'comment')

@admin.register(Lapak)
class LapakAdmin(admin.ModelAdmin):
    list_display = ['id','owner','nama_lapak', 'kategori', 'harga']
    list_filter = ['kategori']
    search_fields = ['nama_lapak', 'deskripsi']

