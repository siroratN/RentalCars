import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from .views import *
from adminrental.forms import *
from django.shortcuts import get_object_or_404, redirect, render
from myrental.models import *

class RentalListView(View):
    def get(self, request):
        rentals = Rental.objects.all().order_by('rental_car__start_date')  # Order by customer ID
        return render(request, 'manage-rent.html', {'rentals': rentals})

class RentalSearch(View):
    def get(self, request):
        search = request.GET.get('search')
        rental = Rental.objects.filter(rental_car__car__make__icontains=search)
        return render(request, "manage-rent.html", {'rentals': rental})
    
class ManageCar(View):
    def get(self, request):
        category = CategoryCar.objects.all().order_by('id') # 5 category ที่เราจะเลือก
        catpk = CategoryCar.objects.get(pk=1) 
        carlists = Car.objects.filter(category=1) # ตาราง default ตอนยังไม่กดเลือก
        return render(request, "manage-car.html", {'category' : category,
                                                   'carlists' : carlists,
                                                   'catpk' : catpk})
    
class SelectCategory(View):
    def get(self, request, pk):
        category = CategoryCar.objects.all()
        carlists = Car.objects.filter(category=pk)
        catpk = CategoryCar.objects.get(pk=pk)
        print(catpk.id)
        return render(request, "manage-car.html", {'category' : category,
                                                   'carlists' : carlists,
                                                   'catpk' : catpk})

class CategorySearch(View):
    def get(self, request, pk):
        print(pk)
        search = request.GET.get('search')
        category = CategoryCar.objects.all()
        catpk = CategoryCar.objects.get(id=pk)
        print(catpk)
        carlists = Car.objects.filter(category_id=pk, make__icontains=search)
        return render(request, "manage-car.html", {'category' : category,
                                                   'carlists' : carlists,
                                                   'catpk' : catpk})


class AddCar(View):
    def get(self, request):
        form = UpdateCarForm()
        return render(request, "add-car.html", {"form": form})

    def post(self, request, pk):
        form = UpdateCarForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage_car')

        return render(request, "add-car.html", {"form": form})

class EditCar(View):
    def get(self, request, car_id):
        caredit = Car.objects.get(pk=car_id)
        form = UpdateCarForm(instance=caredit)
        return render(request, "booking.html", {
            "form": form,
        })

    def post(self, request, booking_id):
        caredit = Car.objects.get(pk=booking_id)
        form = UpdateCarForm(request.POST, instance=caredit)

        if form.is_valid():
            form.save()
            return redirect('add_car')

        return render(request, "add-car.html", {
            "form": form
        })