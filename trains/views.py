from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from .models import Train
from .forms import TrainForm


def home(request):
    trains = Train.objects.all() #получить все записи
    paginator = Paginator(trains, 5)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'objects_list': trains})

class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object' #вроде по умолчанию object
    template_name = 'trains/detail.html'

class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home') # вернуться при успехе
    success_message = 'Поезд создан!' #сообщение

class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('train:home') # вернуться при успехе
    success_message = 'Поезд отредактирован!' #сообщение

class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('train:home') # вернуться при успехе