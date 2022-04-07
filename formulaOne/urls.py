from django.urls import path, include
from django.contrib import admin

from . import views
from .views import article_list


#parece que estas son las urls de la aplicacion

urlpatterns = [
    path('article/', article_list),

]