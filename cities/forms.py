from django import forms
from .models import City

# class CityForm(forms.Form):
#     name = forms.CharField(label = 'город')

class CityForm(forms.ModelForm):
    name = forms.CharField(label = 'Город',
        widget = forms.TextInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите название города!'})) #меняем внешний вид 
    class Meta(object):
        model = City
        fields = ('name', )
