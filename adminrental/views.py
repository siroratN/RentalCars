import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from .views import *
from adminrental.forms import *
from django.shortcuts import get_object_or_404, redirect, render
from myrental.models import *
from django.contrib import messages

class RentalListView(View):
    def get(self, request):
        rentals = Rental.objects.all().order_by('rental_car__start_date')  # Order by customer ID
        return render(request, 'manage-rent.html', {'rentals': rentals})

class RentalSearch(View):
    def get(self, request):
        search = request.GET.get('search')
        rental = Rental.objects.filter(rental_car__car__make__icontains=search)
        return render(request, "manage-rent.html", {'rentals': rental})
    

class CustomerInfo(View):
    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        return render(request, "customer-info.html", {'customer': customer})

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
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = UpdateCarForm(instance=car)
        return render(request, "edit-car.html", {
                               "form": form,
                               "car": car
                               })

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = UpdateCarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            form.save()
            return redirect('manage_car')

        return render(request, "edit-car.html", {
            "form": form,
            "car": car
        })
    
class DeleteCar(View):
    def delete(self, request, pk):
            print(pk)
            car = Car.objects.get(pk=pk)
            car.delete()
            print("xxx")
            return JsonResponse({'status': 'success'})  # Redirect after successful deletion
        # Redirect if car does not exist
        