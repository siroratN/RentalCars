from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from myrental.models import *
from django.contrib.auth.models import Group, User
from .forms import UpdateCarForm, AddEmployeeForm
from django.http import JsonResponse
from django.db.models import F

class RentalListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"

    def get(self, request):
        if request.user.is_staff:
            rentals = Rental.objects.annotate(
                deposit=(F('total_price') * 80) / 100
                )
            print(rentals)

            return render(request, 'manage-rent.html', {'rentals': rentals})
        else:
            raise PermissionDenied

class RentalDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"

    def get(self, request, pk):
        if request.user.is_staff:
            rentals = Rental_car.objects.filter(rental_id = pk)
            print(rentals)
            return render(request, 'rentaldetail.html', {'rental_detail': rentals})
        else:
            raise PermissionDenied

class RentalSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "myrental.view_rental"

    def get(self, request):
        if request.user.is_staff:
            search = request.GET.get('search')
            print(search)
            rental = Rental.objects.filter(customer__user__username__icontains=search)
            return render(request, "manage-rent.html", {'rentals': rental})
        else:
            raise PermissionDenied
    
class AddEmployee(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = "auth.add_user"

    def get(self, request):
        form = AddEmployeeForm()
        return render(request, "add-employee.html", {"form": form})

    def post(self, request):
        form = AddEmployeeForm(request.POST)

        if form.is_valid():
            form = form.save()
            employee_group = Group.objects.get(name="Employee")
            form.groups.add(employee_group)
            form.is_staff = True
            form = form.save()

            return redirect('employee_list')

        return render(request, "add-employee.html", {"form": form})

class EmployeeList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login/'
    permission_required = ['auth.view_user', 'auth.delete_user']
    def get(self, request):
        employee_group = Group.objects.get(name="Employee")
        employees = employee_group.user_set.all()
        return render(request, 'employeelist.html', {
            'employees': employees
        })
    
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return JsonResponse({'status': 'success'})


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

class RefreshSearch(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/login'
    permission_required = "myrental.view_car"

    def get(self, request, pk):
        category = CategoryCar.objects.all()
        catpk = CategoryCar.objects.get(id=pk)
        carlists = Car.objects.filter(category_id=pk)
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
