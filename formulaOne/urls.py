from django.urls import path, include
from django.contrib import admin

from . import views
from .views import comparaciones


#parece que estas son las urls de la aplicacion

urlpatterns = [
    path('comparacion/<int:year>/<str:piloto1>/<str:piloto2>', views.comparaciones, name='comparacion'),

]