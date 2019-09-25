from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from trains.models import Train
from .forms import RouteForm, RouteModelForm
from .models import Route

#функция поиска всех возможных маршрутов в графе
#без повторного посещения одного города
#просто срисовываю с видео
def dfs_path(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop() 
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    #тут я убрал одни скобки и получил ошибку! вернул!
                    stack.append((next_, path + [next_]))

#строим граф на основе записей в БД (5-34)
def get_graph():
    qs = Train.objects.values('from_city') #откуда можно уехать, словарь, повторы
    from_city_set = set(i['from_city'] for i in qs) #разворачиваем в set
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city = city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph

# это главная страница - на ней форма поиска
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})

# поиск маршрута(ов) из города в город
# вывод результатов - /find/, в случае ошибок - на главной странице
def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            #данные получены и валидны
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities']
            travel_time = data['travel_time']
            graph = get_graph()
            all_ways = list(dfs_path(graph, from_city.id, to_city.id))

            # если маршутов нет
            if len(all_ways) == 0:
                messages.error(request, 'Не проехать!((')
                return render(request, 'routes/home.html', {'form': form})

            # если нужно учесть, через какие города
            if across_cities: #меняем формат
                across_cities = [city.id for city in across_cities]
                right_ways = []
                # temp - до этого места работает! #
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if len(right_ways) == 0:
                    messages.error(request, 'Не проехать через все указанные города!((')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            # формируем массив поездов, т.е. по сути - ребер графа
            # не длинным ли путём мы идём?!
            # вот бы сразу сохранить ребра, а не только вершины?)
            trains = []
            for way in right_ways:
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(way)-1):
                    qs = Train.objects.filter(from_city = way[index], to_city = way[index + 1])
                    qs = qs.order_by('travel_time').first() # в случае, если между двумя городами ходит несколько поездов с разным временем в пути
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time # все поезда и время в tmp
                # укладываемся по времени?
                if total_time <= travel_time:
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Нет маршрутов за желаемое время!((')
                return render(request, 'routes/home.html', {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                routes.append({
                    'route': tr['trains'],
                    'total_time': tr['total_time'],
                    'from_city': from_city.name,
                    'to_city': to_city.name
                })
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                # это напоминает какой-то велосипед на костылях
                # это сортировка маршрутов по времени!
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            context = {}
            form = RouteForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities
            return render(request, 'routes/home.html', context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        #данных нет
        messages.error(request, 'Необходимо заполнить форму!')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})

# сохранение одного маршрута из результатов
# работает по адресу add_route
# сначала отрабатывает GET, выводится input для названия
# потом POST и происходит запись
def add_route(request):
    if request.method == 'POST':
        # здесь сохраняем данные
        # assert False # для просмотра данных
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            from_city = data['from_city']
            to_city = data['to_city']
            travel_time = data['travel_time']
            trains = data['trains'].split(' ')
            trains = [int(x) for(x) in trains if x.isalnum()]
            qs = Train.objects.filter(id__in = trains)
            route = Route(name=name, from_city=from_city,
                    to_city=to_city, travel_time=travel_time)
            route.save() # сохраняем без поездов
            # trains - массив, поэтому попробую обойти его, а не qs
            # не получилось - делаю как в курсе
            for train in qs:
                #route.trains.add(train)
                route.trains.add(train.id)
            messages.success(request, 'Маршрут успешно сохранён!')
            return redirect('/')
        else:
            # форма не валидна
            print (form)
            messages.error(request, 'Форма не прошла валидацию!')
            return redirect('/')
    elif request.method == 'GET':
        # сюда попадает даже если GET пустой, поэтому добавил if data - по сути, надо было делать как в уроке!
        # здесь предлагаем ввести имя, выводим данные маршрута
        # и их же в скрытых полях формы
        data = request.GET
        if data:
            from_city = data['from_city']
            to_city = data['to_city']
            travel_time = data['travel_time']
            trains = data['trains'].split(' ')
            # избавляемся от пробелов
            trains = [int(x) for(x) in trains if x.isalnum()]
            trains_str = ' '.join(str(i) for i in trains)
            #получаем поезда по их id
            qs = Train.objects.filter(id__in = trains)
            form = RouteModelForm(initial = {
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time,
                'trains': trains_str, #пытался передать массив - не прокатило!(
            })
            desc = []
            for train in qs:
                dsc = '''Поезд №{}, из {} в {}
                        (время в пути - {})'''.format(train.name, train.from_city,
                                                train.to_city, train.travel_time)
                desc.append(dsc)
            context = {
                'form': form,
                'desc': desc,
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time,
            }
            return render(request, 'routes/create.html', context)
        else:
            # не пришло ничего
            messages.error(request, 'Невозможно сохранить - данные не пришли!')
            return redirect('/')

class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object' #вроде по умолчанию object
    template_name = 'routes/detail.html'

class RouteListlView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'objects_list'
    template_name = 'routes/list.html'

class RouteDeleteView(DeleteView):
    model = Route
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('home') # вернуться при успехе