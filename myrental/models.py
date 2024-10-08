from django.db import models
from django.contrib.auth.models import User

class CategoryCar(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=100)
    
class Feature(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price_per_day = models.IntegerField()
    description = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryCar, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)
    feature = models.ManyToManyField(Feature)
    def __str__(self):
        return f"{self.make} {self.model}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Rental(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Rental_car(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


