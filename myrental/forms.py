# forms.py
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from .models import *


# class   CarImageForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         field = ['']

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
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
        
    
