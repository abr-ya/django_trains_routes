from django.db import models

class City(models.Model):
    #verbose_name - название на странице записи
    name = models.CharField(max_length=100, unique=True, verbose_name='Город (один)')

    def __str__(self):
        return self.name

    #переименовать в админке
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
