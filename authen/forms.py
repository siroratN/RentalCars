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

