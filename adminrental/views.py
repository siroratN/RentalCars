from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from myrental.models import Rental, Customer, CategoryCar, Car
from .forms import UpdateCarForm
from django.http import JsonResponse

class RentalListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"

    def get(self, request):
        rentals = Rental.objects.all().order_by('rental_car__start_date')
        return render(request, 'manage-rent.html', {'rentals': rentals})

class RentalSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"

    def get(self, request):
        search = request.GET.get('search')
        rental = Rental.objects.filter(rental_car__car__make__icontains=search)
        return render(request, "manage-rent.html", {'rentals': rental})

class CustomerInfo(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_customer"

    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        return render(request, "customer-info.html", {'customer': customer})

class ManageCar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_car"

    def get(self, request):
        category = CategoryCar.objects.all().order_by('id')
        catpk = CategoryCar.objects.get(pk=1)
        carlists = Car.objects.filter(category=1)
        return render(request, "manage-car.html", {'category': category,
                                                   'carlists': carlists,
                                                   'catpk': catpk})

class SelectCategory(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_car"

    def get(self, request, pk):
        category = CategoryCar.objects.all()
        carlists = Car.objects.filter(category=pk)
        catpk = CategoryCar.objects.get(pk=pk)
        return render(request, "manage-car.html", {'category': category,
                                                   'carlists': carlists,
                                                   'catpk': catpk})

class CategorySearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login'
    permission_required = "myrental.view_car"

    def get(self, request, pk):
        search = request.GET.get('search')
        category = CategoryCar.objects.all()
        catpk = CategoryCar.objects.get(id=pk)
        carlists = Car.objects.filter(category_id=pk, make__icontains=search)
        return render(request, "manage-car.html", {'category': category,
                                                   'carlists': carlists,
                                                   'catpk': catpk})

class AddCar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.add_car"

    def get(self, request):
        form = UpdateCarForm()
        return render(request, "add-car.html", {"form": form})

    def post(self, request):
        form = UpdateCarForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage_car')

        return render(request, "add-car.html", {"form": form})

class EditCar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.change_car"

    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = UpdateCarForm(instance=car)
        return render(request, "edit-car.html", {"form": form, "car": car})

    def post(self, request, pk):
        car = Car.objects.get(pk=pk)
        form = UpdateCarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            form.save()
            return redirect('manage_car')

        return render(request, "edit-car.html", {"form": form, "car": car})

class DeleteCar(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.delete_car"

    def delete(self, request, pk):
        car = Car.objects.get(pk=pk)
        car.delete()
        return JsonResponse({'status': 'success'})
