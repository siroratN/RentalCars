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

class RentalView(View):
    def get(self, request):
        cate = CategoryCar.objects.all()
        car = Car.objects.all()
        feature = Feature.objects.all()
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        datetime.datetime.strptime(start, "%Y-%m-%d").date()
        datetime.datetime.strptime(end, "%Y-%m-%d").date()
        ans = Car.objects.annotate(
        rental_count=Count('rental')
        ).filter(
            Q(rental__rental_car__start_date__gt=end) | 
            Q(rental__rental_car__end_date__lt=start) |
            Q(rental_count=0) #รถที่ไม่ได้เช่า
        )        
        return render(request, "homeren.html", {'cate': cate, "car":car, "feature": feature})
    
# class RentalView(View):
#     def post(self, request, start_date, end_date):
#         print(start_date)
#         response_data = {
#             'start_date': start_date,
#             'end_date': end_date,
#             'message': 'Rental request received!'
#         }
#         return JsonResponse(response_data)

class CarDetail(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        return render(request, 'CarDetail.html', {'car':car})
class ConfirmBill(View):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        return render(request, 'confirm.html' , {'car':car, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,})