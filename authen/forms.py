# forms.py

from django import forms
from django.contrib.auth.models import User
from myrental.models import Customer

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
               'placeholder': 'Password'}))
    
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
               'placeholder': 'Phone'}))
    
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
               'placeholder': 'Address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
                'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
                'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
                'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={
                'class': 'w-full text-sm text-gray-800 bg-gray-100 focus:bg-transparent px-4 py-3.5 rounded-md outline-blue-600', 
                'placeholder': 'Email'}),
        }
