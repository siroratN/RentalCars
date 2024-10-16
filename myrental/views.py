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


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    login_url = '/authen/login/'
    def post(self, request):
        try:
            YOUR_DOMAIN = 'http://127.0.0.1:8000'
            data = json.loads(request.body)
            price = data.get('price')
            car_ids = data.get('car_id')
            print('yyy',car_ids)
            start_dates = data.get('start_date')
            end_dates = data.get('end_date')

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'thb',
                        'unit_amount': int((price*20/100) * 100),
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
                    'car_ids': json.dumps(car_ids),  #เก็บเป็น str
                    'start_dates': json.dumps(start_dates),
                    'end_dates': json.dumps(end_dates),
                }
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Success(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = ["myrental.add_rental", "myrental.add_rental_car"]
    def get(self, request):
        try:
            checkout_session_id = request.GET.get('checkout_session_id')
            checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)  # เอาข้อมูลออกมา
            price = checkout_session['amount_total'] 
            deposit = price / 100 #เงินมัดจำ 
            total_price = deposit / 0.2 
            car_ids = json.loads(checkout_session['metadata']['car_ids'])
            start_dates = json.loads(checkout_session['metadata']['start_dates'])
            end_dates = json.loads(checkout_session['metadata']['end_dates'])
            cus = Customer.objects.get(user=request.user.id)
            newrental = Rental.objects.create(
                customer=cus,
                total_price=total_price,
                status='Complete',
                checkout_session_id= checkout_session_id)
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
            rental= Rental.objects.filter(pk=newrental.id).annotate(
            deposit=(F('total_price') * 0.2)).first()
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
                'rental': rental,
                'allren': allren,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Cancel(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"
    def get(self, request):
        return render(request, 'cancel.html')
    def put(self, request, rental_id):
        print('fkk')
        print(rental_id)
        try:
            rental = Rental.objects.get(id=rental_id)
            rental.status = 'Cancel'
            rental.save()
            print(rental.checkout_session_id)
            checkout_session = stripe.checkout.Session.retrieve(rental.checkout_session_id)
            payment_intent_id = checkout_session.payment_intent
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
            )
            return JsonResponse({"cancel": "success"})
        except Rental.DoesNotExist:
            return JsonResponse({'error': 'Rental not found'}, status=404)
        

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
        rental_car__start_date__lte=end_date,
        rental_car__end_date__gte=start_date 
    )

class RentalViewFirst(View):
    def get(self, request):
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def filter_cars(available_cars, categories, brands, features, price):
            if categories:
                available_cars = available_cars.filter(category__id__in=categories)
            if brands:
                available_cars = available_cars.filter(make__in=brands)
            if features:
                available_cars = available_cars.filter(feature__id__in=features)
            return available_cars.filter(price_per_day__lte=price)
        
class FilterView(View):

    def get(self, request, start_date, end_date):
        try:
            cate = CategoryCar.objects.all().distinct()
            car = Car.objects.values('make').distinct()
            feature = Feature.objects.all().distinct()
            
            selected_categories = [int(cat_id) for cat_id in request.GET.getlist('categories')]
            print(selected_categories)
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
class SearchView( View):
        def get(self, request, start_date, end_date):
            try:
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
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

class CarDetail(View):
    def get(self, request, pk, start_date, end_date):
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            print('check')
            print(end_date)
            car = Car.objects.get(pk=pk)
            return render(request, 'CarDetail.html', {'car':car, 'start_date':start_date, 'end_date':end_date})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class ConfirmBill(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"  
    def get(self, request, pk):
        try:
            car = Car.objects.get(pk=pk)
            cus = Customer.objects.get(user=request.user.id)
            return render(request, 'confirm.html' , {'car':car,'cus':cus, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
class RentHistory(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = ["myrental.view_rental", "myrental.view_rental_car"]
    
    def get(self, request):
        try:
            cus = Customer.objects.get(user=request.user.id)
            rentals = Rental.objects.filter(customer_id=cus.id)

            rental_data = []
            can_cancel = True
            current_date = timezone.now().date()

            for rental in rentals:
                rental_cars = Rental_car.objects.filter(rental=rental)
                can_cancel_rental = True

                for i in rental_cars:
                    if i.start_date <= current_date:
                        can_cancel_rental = False

                rental_data.append({
                    'rental': rental,
                    'rental_cars': rental_cars,
                    'can_cancel': can_cancel_rental
                })
            print(rental_data)

            return render(request, 'rent-history.html', {
                'rental_data': rental_data,
                'cancel': can_cancel
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)