from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserLoginForm

#не используется
def home_view(request):
    context = {'name': 'Name2'} #словарь передается в шаблон
    return render(request, 'home.html', context) #рендер: запрос, шаблон, словарь
                                                #путь к папке шаблонов - в настройках

#логин
def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'login.html', {'form': form})

#логаут
def logout_view(request):
    logout(request)
    return redirect('home')