from django import forms
from django.forms import formset_factory
from .models import *
from django.contrib.auth.models import User


class Checkoutform(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']
        widgets = {
            'ordered_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Name '
            }),
            'shipping_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Address'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Id',
            })
        }


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Password'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email Id'
    }))

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'address']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Full Name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your address'
            }),
        }

        def clean_username(self):
            uname = self.cleaned_data.get('username')
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError(
                    "Username taken bt another customer, Try again!")
            return uname


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Password'
    }))


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Password'
    }))


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': True
    }))

    class Meta:
        view_status = (
            ("Order_Received", "Order_Received"),
            ("Order_Processing", "Order_Processing"),
            ("On_The_Way", "On_The_Way"),
            ("Order_Completed", "Order_Completed"),
            ("Order_Canceled", "Order_Canceled"),
        )
        model = Product
        fields = ['title', 'slug', 'category', 'image', 'marked_price',
                  'selling_price', 'description', 'warranty', 'return_policy']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Title '
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Unique Slug '
            }),
            'Category': forms.ChoiceField(choices=view_status),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'marked_price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Marked Price '
            }),
            'selling_price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Selling Price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'warranty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Warranty'
            }),

            'return_policy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write Replacement Policy'
            }),

        }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter Registered Email',
               'class': 'form-control'
               }))

    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError("Email Does Not exists!")
        return e
