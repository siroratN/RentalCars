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
from django.http import JsonResponse, HttpResponse
from django.views import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(View):
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


class Success(View):
    def get(self, request):
        checkout_session_id = request.GET.get('checkout_session_id')
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id) #ดึงข้อมูลทั้งหมด
        total_price = checkout_session['amount_total']
        car_ids = json.loads(checkout_session['metadata']['car_ids'])
        start_dates = json.loads(checkout_session['metadata']['start_dates'])
        end_dates = json.loads(checkout_session['metadata']['end_dates']) #แปลงกลับเป็น list
        print(start_dates)
        cus = Customer.objects.get(user=request.user.id)
        status = checkout_session['payment_status']
        if status == 'paid':
            newrental = Rental.objects.create(
                customer=cus,
                total_price=int(total_price)/100,
                status='Complete')
            print(newrental)
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
            for i in allren:
                print(i.start_date)
            return render(request, 'success.html', {
                'rental': newrental,
                'allren': allren
            })
        else:
            return render(request, 'cancel.html')

class Cancel(View):
    def get(self, request):
        return render(request, 'cancel.html')

class DateRental(View): 
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
        rental_car__start_date__lt=end_date,
        rental_car__end_date__gt=start_date 
    )
class RentalViewFirst(View):
    def get(self, request):
        cate = CategoryCar.objects.all()
        car = Car.objects.all()
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
        
class FilterView(View):
    def get(self, request, start_date, end_date):
        cate = CategoryCar.objects.all()
        car = Car.objects.all()
        feature = Feature.objects.all()
        selected_categories = [int(cat_id) for cat_id in request.GET.getlist('categories')]
        selected_brands = request.GET.getlist('brands')
        selected_features = [int(feature_id) for feature_id in request.GET.getlist('features')]
        selected_price = request.GET.get('price')
        selected_price = int(selected_price) if selected_price else 8500
        print(selected_price)
        datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        available_cars = get_available_cars(start_date, end_date)
        if selected_categories:
            available_cars = available_cars.filter(category__id__in=selected_categories)
        if selected_brands:
            available_cars = available_cars.filter(make__in=selected_brands)
        if selected_features:
            available_cars = available_cars.filter(feature__id__in=selected_features)
        if selected_price:
            available_cars = available_cars.filter(price_per_day__lte=selected_price)
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
        
class SearchView(View):
        def get(self, request, start_date, end_date):
            cate = CategoryCar.objects.all()
            car = Car.objects.all()
            feature = Feature.objects.all()
            car_search = request.GET.get('car')
            datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
            available_cars = get_available_cars(start_date, end_date)
            available_cars = available_cars.filter(make__icontains=car_search)
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

class CarDetail(View):
    def get(self, request, pk, start_date, end_date):
        datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        print('check')
        print(end_date)
        car = Car.objects.get(pk=pk)
        return render(request, 'CarDetail.html', {'car':car, 'start_date':start_date, 'end_date':end_date})

class ConfirmBill(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        subject = 'Your Car Booking Confirmation'
        cus = Customer.objects.get(user=request.user.id)
        message = f"""
        เรียนคุณ {cus.user.username},
        การจองรถ {car} ของคุณได้รับการยืนยันแล้ว
        หากคุณมีคำถามหรือต้องการความช่วยเหลือเพิ่มเติม กรุณาติดต่อเราที่เบอร์ 038-456-987
        ทางร้านจะติดต่อกลับไปหาคุณเร็วๆ นี้
        ขอบคุณที่ใช้บริการเรา!
        """ 
        recipient_list = [request.user.email]
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, 
            recipient_list,
            fail_silently=False,
        )
        return render(request, 'confirm.html' , {'car':car,'cus':cus, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,})