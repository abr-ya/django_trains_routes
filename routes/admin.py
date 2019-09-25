from django.contrib import admin
from .models import Route

# class RouteAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Route
#     list_display = ['name']
#     # редактирование при отображении
#     list_editable = ['name']

admin.site.register(Route)
#admin.site.register(Route, RouteAdmin)
