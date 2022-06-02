from django.urls import path, include
from django.contrib import admin

from . import views


#parece que estas son las urls de la aplicacion

urlpatterns = [
    path('comparaciones/<int:year>/<str:piloto1>/<str:piloto2>', views.comparacion, name='comparacion'),

]