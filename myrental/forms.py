# forms.py
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils import timezone

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5',
            'placeholder': 'Select date start',
            'id': 'start_date',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5',
            'placeholder': 'Select date end',
            'id': 'end_date',
            'type': 'date'
        })
    )
    def clean(self):
        cleaned_data = super().clean()
        end_date = cleaned_data["end_date"]
        start_date = cleaned_data["start_date"]
        if start_date < timezone.now().date():
            raise ValidationError("ห้ามเลือกวันก่อนวันปัจจุบัน")
        if end_date < start_date:
            raise ValidationError("ห้ามเลือกวันสิ้นสุดก่อนวันเริ่ม")
        return cleaned_data
        
    
