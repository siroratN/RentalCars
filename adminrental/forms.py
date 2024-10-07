from django import forms
from myrental.models import *

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price_per_day', 'description', 'category', 'image', 'feature']