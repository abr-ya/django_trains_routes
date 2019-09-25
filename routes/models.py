from django.db import models
from trains.models import Train

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')
    from_city = models.CharField(max_length=100, unique=True, verbose_name='Откуда')
    to_city = models.CharField(max_length=100, unique=True, verbose_name='Куда')
    #across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через города') #было
    trains = models.ManyToManyField(Train, blank=True, verbose_name='Поезда') #стало
    travel_time = models.IntegerField(verbose_name='Время в пути')
    # from_city = models.ForeignKey(City, on_delete=models.CASCADE,
    #    verbose_name='Откуда', related_name='from_city')
    #to_city = models.ForeignKey(City, on_delete=models.CASCADE,
    #    verbose_name='Куда', related_name='to_city')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']

    #отображение
    def __str__(self):
        return self.name