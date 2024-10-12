import json
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.http import *
from .forms import *
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import *
import datetime
from django.db.models import *
import json
from django.http import JsonResponse
from django.views import View
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CreateCheckoutSessionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental" 
    def post(self, request):
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        data = json.loads(request.body)
        price = data.get('price')
        car_ids = data.get('car_id')
        start_dates = data.get('start_date')
        end_dates = data.get('end_date')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'thb',
                    'unit_amount': int(price * 100),
                    'product_data': {
                        'name': "car"
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{YOUR_DOMAIN}/success/?checkout_session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{YOUR_DOMAIN}/cancel/',
            metadata={
                'car_ids': json.dumps(car_ids), # เก็บผ่าน str
                'start_dates': json.dumps(start_dates),
                'end_dates': json.dumps(end_dates),
            }
        )
        return JsonResponse({'id': checkout_session.id})


class Success(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental" 
    def get(self, request):
        checkout_session_id = request.GET.get('checkout_session_id')
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id) #ดึงข้อมูลทั้งหมด
        total_price = checkout_session['amount_total']
        car_ids = json.loads(checkout_session['metadata']['car_ids'])
        start_dates = json.loads(checkout_session['metadata']['start_dates'])
        end_dates = json.loads(checkout_session['metadata']['end_dates'])
        print(checkout_session['metadata'])
        print(start_dates)
        cus = Customer.objects.get(user=request.user.id)
        newrental = Rental.objects.create(
            customer=cus,
            total_price=int(total_price)/100,
            status='Complete')
        for i in range(len(car_ids)):
            car = Car.objects.get(id=car_ids[i])
            start_date = start_dates[i]
            end_date = end_dates[i]
            Rental_car.objects.create(
                rental=newrental,
                car=car,
                start_date=start_date,
                end_date=end_date
            )
        allren = Rental_car.objects.filter(rental=newrental)
        car_names = ', '.join([str(rental_car.car) for rental_car in allren])
        
        subject = 'Your Car Booking Confirmation'
        message = f"""
    เรียนคุณ {cus},
การจองรถ {car_names} ของคุณได้รับการยืนยันแล้ว
หากคุณมีคำถามหรือต้องการความช่วยเหลือเพิ่มเติม กรุณาติดต่อเราที่เบอร์ 038-456-987
ทางร้านจะติดต่อกลับไปหาคุณเร็วๆ นี้
ขอบคุณที่ใช้บริการเรา!
""" 
        recipient_list = [request.user.email]
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, 
            recipient_list
        )
        
        return render(request, 'success.html', {
                'rental': newrental,
                'allren': allren
            })

class Cancel(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"
    def get(self, request):
        return render(request, 'cancel.html')

class DateRental(LoginRequiredMixin, PermissionRequiredMixin, View): 
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"
    def get(self, request):
        form = DateRangeForm()
        return render(request, "date.html", {"form" : form})
    def post(self, request):
        form = DateRangeForm(request.POST)
        print(form)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            return redirect(f'/rental/?start_date={start_date}&end_date={end_date}')
        return render(request, "date.html", {"form" : form})

def get_available_cars(start_date, end_date):

    return Car.objects.exclude(
        rental_car__start_date__lte=end_date,
        rental_car__end_date__gte=start_date 
    )

class RentalViewFirst(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"  
    def get(self, request):
        cate = CategoryCar.objects.all().distinct()
        car = Car.objects.values('make').distinct()
        feature = Feature.objects.all()

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        available_cars = get_available_cars(start_date, end_date)
        return render(request, "homeren.html", {
            'cate': cate,
            'car': car,
            'feature': feature,
            'cars': available_cars,
            'start_date': start_date,
            'end_date': end_date,
        })
        
class FilterView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"
    def get(self, request, start_date, end_date):
        
        cate = CategoryCar.objects.all().distinct()
        car = Car.objects.values('make').distinct()
        feature = Feature.objects.all().distinct()
        
        selected_categories = [int(cat_id) for cat_id in request.GET.getlist('categories')]
        selected_brands = request.GET.getlist('brands')
        selected_features = [int(feature_id) for feature_id in request.GET.getlist('features')]
        selected_price = request.GET.get('price')
        selected_price = int(selected_price) if selected_price else 8500
        print(selected_price)
        
        datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        available_cars = get_available_cars(start_date, end_date)
        
        available_cars = filter_cars(get_available_cars(start_date, end_date), selected_categories, selected_brands, selected_features, selected_price)

        if not available_cars.exists():
            message = "ไม่พบรถที่ต้องการค้นหา"
        else:
            message = None
            
        return render(request, "homeren.html", {
            'cate': cate,
            'car': car,
            'feature': feature,
            'cars': available_cars,
            'start_date': start_date,
            'end_date': end_date,
            'selected_categories': selected_categories,
            'selected_brands': selected_brands,
            'selected_features': selected_features,
            'selected_price': selected_price,
            'message': message
        })
        
class SearchView(LoginRequiredMixin, PermissionRequiredMixin, View):
        login_url = '/authen/login/'
        permission_required = "myrental.view_rental"
        def get(self, request, start_date, end_date):
            cate = CategoryCar.objects.all().distinct()
            car = Car.objects.values('make').distinct()
            feature = Feature.objects.all().distinct()
            
            car_search = request.GET.get('car')
            
            datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
            available_cars = get_available_cars(start_date, end_date).filter(make__icontains=car_search)
            print(available_cars)
            
            if not available_cars.exists():
                message = "ไม่พบรถที่ต้องการค้นหา"
            else:
                message = None
                
            return render(request, "homeren.html", {
            'cate': cate,
            'car': car,
            'feature': feature,
            'cars': available_cars,
            'start_date': start_date,
            'end_date': end_date,
            'car_search': car_search,
            'message': message
        })   

class CarDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"
    def get(self, request, pk, start_date, end_date):
        datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        print('check')
        print(end_date)
        car = Car.objects.get(pk=pk)
        return render(request, 'CarDetail.html', {'car':car, 'start_date':start_date, 'end_date':end_date})

class ConfirmBill(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"  
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        cus = Customer.objects.get(user=request.user.id)
        return render(request, 'confirm.html' , {'car':car,'cus':cus, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,})