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


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'thb', 
                        'unit_amount': int(car.price_per_day * 100), 
                        'product_data': {
                            'name': car
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })
        
class Success(View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        print(checkout_session)
        print(checkout_session['payment_status'])
        status = checkout_session['payment_status']
        if status == 'paid':
            return HttpResponse("Payment succeeded!")
        elif status == 'pending':
            return HttpResponse("Payment is still processing.")
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
        return Car.objects.annotate(rental_count=Count('rental')).filter(
            Q(rental__rental_car__start_date__gt=end_date) | 
            Q(rental__rental_car__end_date__lt=start_date) | 
            Q(rental_count=0)
        )

class RentalView(View):
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
            'selected_price': selected_price
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
            
            return render(request, "homeren.html", {
            'cate': cate,
            'car': car,
            'feature': feature,
            'cars': available_cars,
            'start_date': start_date,
            'end_date': end_date,
            'car_search': car_search
            
        })
            
            

class CarDetail(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        return render(request, 'CarDetail.html', {'car':car})

class ConfirmBill(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        return render(request, 'confirm.html' , {'car':car, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,})