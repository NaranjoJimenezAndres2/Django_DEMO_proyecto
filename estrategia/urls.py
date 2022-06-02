from django.urls import path, include
from django.contrib import admin

from . import views
from .views import estrategia
#from .views import actividad_list


#parece que estas son las urls de la aplicacion

urlpatterns = [
   path('stints/<str:piloto1>/<str:gp>/<str:year>', views.estrategia), 

]