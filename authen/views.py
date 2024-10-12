from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from myrental.models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)

            if user.is_staff:
                return redirect('rental_info')
            else:
                return redirect('Date')
        return render(request,'login.html', {"form":form})


class RegisterView(View):
    
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)        
        if user_form.is_valid():
            user = user_form.save()
            customer = Customer.objects.create(
                user=user,
                phone_number=user_form.cleaned_data['phone_number'],
                address=user_form.cleaned_data['address']
            )
            customer.save()
            return redirect('login')
        return render(request, 'register.html', {'user_form': user_form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')
    
class ProfileView(View):
    def get(self, request):
        user_form = UserProfileForm(instance=request.user)
        customer_form = CustomerProfileForm(instance=request.user.customer)
        
        return render(request, 'profile.html', {
            'user_form': user_form,
            'customer_form': customer_form
        })
    
    def post(self, request):
        user_form = UserProfileForm(request.POST, instance=request.user)
        customer_form = CustomerProfileForm(request.POST, instance=request.user.customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            message = 'บันทึกการเปลี่ยนแปลงเรียบร้อย!'
        else:
            message = 'ผิดพลาดในการบันทึก!'
        return render(request, 'profile.html', {
            'user_form': user_form,
            'customer_form': customer_form,
            'message': message
        })
    
class PasswordChangeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = PasswordChangeForm(user=request.user)
        return render(request, 'changePass.html', {'form': form})
    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            message = 'รหัสผ่านของคุณถูกเปลี่ยนเรียบร้อยแล้ว!'
        else:
            message = 'ผิดพลาดในการเปลี่ยนรหัสผ่าน!'
        return render(request, 'changePass.html', {'form': form, 'message': message})