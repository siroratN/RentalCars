from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import *


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('Date')  
        return render(request,'login.html', {"form":form})


class RegisterView(View):
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

        
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            customer = Customer.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            customer.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')