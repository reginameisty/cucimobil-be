from django import forms
from .models import Order, Customer, Lapak
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'
        
    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
        return order
    
class CustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    password = forms.CharField(widget=forms.PasswordInput)

class LapakForm(forms.ModelForm):
    class Meta:
        model = Lapak
        fields = ['foto', 'nama_lapak', 'kategori', 'harga', 'deskripsi']