from django import forms
from myrental.models import *

class UpdateCarForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Allow image upload

    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price_per_day', 'description', 'category', 'feature', 'image']
        widgets = {
            'feature': forms.CheckboxSelectMultiple(),  # ทำให้ feature เป็นแบบ multiple choice
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and year > 2024:
            raise forms.ValidationError('Year cannot be in the future.')
        return year

