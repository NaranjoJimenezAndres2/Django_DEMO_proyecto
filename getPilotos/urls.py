from django.urls import path, include
from django.contrib import admin

from . import views
from .views import getpilotos
#from .views import actividad_list


#parece que estas son las urls de la aplicacion

urlpatterns = [
   path('getPilotos/<int:year>', views.getpilotos), 

]