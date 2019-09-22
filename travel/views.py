from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    context = {'name': 'Name2'} #словарь передается в шаблон
    return render(request, 'home.html', context) #рендер: запрос, шаблон, словарь
                                                #путь к папке шаблонов - в настройках
