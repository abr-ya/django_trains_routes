"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from .views import home_view
from routes.views import home, find_routes, add_route
from routes.views import RouteListlView, RouteDetailView, RouteDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include(('cities.urls', 'city'))), #похоже, здесь задается пространство имён 'city'
                                                    #используется в boot при построении url
	path('trains/', include(('trains.urls', 'train'))),
    #path('', home_view, name='home'),
    path('', home, name='home'),
    path('find/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('routes/', RouteListlView.as_view(), name='routes'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
]
