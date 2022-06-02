from django.urls import path, include
from django.contrib import admin

from . import views
from .views import telemetria


#parece que estas son las urls de la aplicacion

urlpatterns = [
    path('telemetria/<str:piloto1>/<str:piloto2>/<str:gp>/<str:year>', views.telemetria),

]