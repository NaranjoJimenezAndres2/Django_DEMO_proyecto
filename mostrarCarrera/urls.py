from django.urls import path, include
from django.contrib import admin

from . import views
from .views import carreras
#from .views import actividad_list


#parece que estas son las urls de la aplicacion

urlpatterns = [
   path('resultado/<str:year>/<str:nombreCircuito>', views.carreras), 

]