from django import forms
from myrental.models import Car, Feature
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

class UpdateCarForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput() 
    )
    feature = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price_per_day', 'description', 'category', 'feature', 'image']

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and year > datetime.now().year:    
            raise forms.ValidationError('ไม่สามารถเป็นปีในอนาคตได้')
        return year
    
class AddEmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    
