import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from .views import *
from .models import *
from .forms import *
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
        # rental = Rental.objects.filter(rental_car__icontains=search)
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
        search = request.GET.get('search')
        print(pk)
        category = CategoryCar.objects.all()
        catpk = Car.objects.filter(category=pk)
        carlists = CategoryCar.objects.filter(car__make__icontains=search)
        return render(request, "manage-car.html", {'category' : category,
                                                   'carlists' : carlists,
                                                   'catpk' : catpk})

class AddCar(View):
    def get(self, request):
        return render(request, "add-car.html", )
    
class EditCar(View):
    def get(self, request):
        return render(request, "edit-car.html", )