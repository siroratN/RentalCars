from django import forms
from myrental.models import Car, Feature  # นำเข้าโมเดล Feature ด้วย

class UpdateCarForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={})  # Set your Tailwind classes here
    )
    feature = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),  # ดึงข้อมูลฟีเจอร์ทั้งหมด
        required=False,  # ทำให้ฟิลด์ feature เป็น optional
        widget=forms.CheckboxSelectMultiple()  # ทำให้ feature เป็นแบบ multiple choice
    )

    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price_per_day', 'description', 'category', 'feature', 'image']

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and year > 2024:    
            raise forms.ValidationError('Year cannot be in the future.')
        return year
