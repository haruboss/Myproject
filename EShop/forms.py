from django import forms
from .models import *
from django.contrib.auth.models import User

class Checkoutform(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'address']

        def clean_username(self):
            uname = self.cleaned_data.get('username')
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError("username already taken by another customer")
            return uname

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class' : 'form-control',
        'multiple' : True
    }))
    class Meta:
        model = Product
        fields = ['title', 'slug', 'Category', 'image', 'marked_price', 'selling_price', 'description', 'warranty', 'return_policy']