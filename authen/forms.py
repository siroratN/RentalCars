# forms.py
from django import forms
from django.contrib.auth.models import User
from myrental.models import Customer
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ,'phone_number','address']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address']
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('กรุณากรอกเฉพาะตัวเลขเท่านั้น')
        return phone_number