from django import forms
from .models import Train
from cities.models import City

class TrainForm(forms.ModelForm):
    class Meta(object):
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')    
    name = forms.CharField(label = 'Поезд',
        widget = forms.TextInput(
            attrs={'class': 'form-control',
            'placeholder': 'Введите номер поезда!'})) #меняем внешний вид
    from_city = forms.ModelChoiceField(label = 'Откуда', queryset = City.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control',
            'placeholder': 'Выберите город'}))
    to_city = forms.ModelChoiceField(label = 'Куда', queryset = City.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control',
            'placeholder': 'Выберите город'}))
    travel_time = forms.IntegerField(label = 'Поезд',
        widget = forms.NumberInput(
            attrs={'class': 'form-control',
            'placeholder': 'время в пути'}))

