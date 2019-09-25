from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from .models import City
from .forms import CityForm

def home(request):
    cities = City.objects.all() #получить все записи
    paginator = Paginator(cities, 5)
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    return render(request, 'cities/home.html', {'objects_list': cities})

class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object' #вроде по умолчанию object
    template_name = 'cities/detail.html'

class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home') # вернуться при успехе
    success_message = 'Город создан!' #сообщение

class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:home') # вернуться при успехе
    success_message = 'Город отредактирован!' #сообщение

class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('city:home') # вернуться при успехе