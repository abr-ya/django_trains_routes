from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse

from routes import views as routes_views
from cities.models import City
from trains.models import Train

class RouteTestCase(TestCase):
    def setUp(self):
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        t1 = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        t2 = Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8)
        t3 = Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7)
        t4 = Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6)
        t5 = Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3)
        t6 = Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11)
        t7 = Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10)
        t8 = Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5)
        t9 = Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4)
        t1.save()
        t2.save()
        t3.save()
        t4.save()
        t5.save()
        t6.save()
        t7.save()
        t8.save()
        t9.save()

    # тест создания города с таким же именем,
    # проверка сомнительна
    def test_model_city_duplicate(self):
        try:
            a_city = City(name='A')
            a_city.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Город с таким Город (один) уже существует.']}, e.message_dict)

    # проверка отображения страницы home
    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        print(response.resolver_match.func)

    # кол-во маршрутов из A в E
    def test_count_A2E(self):
        graph = routes_views.get_graph()
        all_ways = list(routes_views.dfs_path(graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_ways), 4)
