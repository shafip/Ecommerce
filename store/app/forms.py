from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(r"^(?=.*[a-zA-Z])[a-zA-Z0-9]+$", "Name should contain only letters, numbers or underscores"),
            validators.MinLengthValidator(3, "Name should have at least 3 characters")
        ],
        error_messages={
            'required': 'The name field is required.',
        }
    )

    class Meta:
        model = Product
        fields = ['name']


class SubProductForm(forms.ModelForm):
    class Meta:
        model = Varient
        fields = ['image','image2','image3','banner','product', 'quantity', 'brand', 'price','stock']


class ShippingForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
                           validators=[validators.MinLengthValidator(3)])
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
                           validators=[validators.MinLengthValidator(3)])
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'pincode'}),
                              validators=[validators.RegexValidator(regex='^[0-9]{6}$',
                                                                    message='Pincode should be a 6 digit number')])
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
                            validators=[validators.RegexValidator(regex='^[0-9]{10}$',
                                                                  message='Phone number should be a 10 digit number')])
    is_defualt = forms.BooleanField(required=False)


    class Meta:
        model = Shipping
        fields = ['name', 'city', 'address', 'pincode', 'phone','is_defualt']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
    )

    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )

    phone_number = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter Phone number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
    )

    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password1'}),
    )

    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

    class Meta:
        model = Users
        fields = ['name', 'email', 'phone_number', 'password1', 'password2']


class ShippingForms(forms.Form):
    selected_item = forms.IntegerField(widget=forms.RadioSelect)
    shipping_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ShippingForms, self).__init__(*args, **kwargs)
        self.fields['selected_item'].choices = [(item.id, item.name) for item in
                                                Shipping.objects.filter(user=self.user)]


from django import forms
from django.contrib.auth.forms import PasswordResetForm


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))


class UsersEditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'image', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class PswdForm(forms.ModelForm):
    password = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password1'}),
    )

    confirm_password = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = Users
        fields = ['password', 'confirm_password']


from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Username '})
    )

    # Example: Override a field widget for password field
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-class', 'placeholder': 'Password '})
    )


from django.contrib.auth.forms import PasswordChangeForm


# class MyPasswordChangeForm(PasswordChangeForm):
#     # Add any additional fields or validation here, if needed
#     pass

class MyPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'custom-class', 'placeholder': 'Password '}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'custom-class', 'placeholder': 'Password '}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'custom-class', 'placeholder': 'Password '}))

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "New passwords do not match.")

        return cleaned_data

class ProductFilterForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        empty_label='Select Product',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
