from django.contrib import admin
from .models import Comparacion  #creo que esto es lo mismo que importarlo de la misma forma que en el serializer

# Register your models here.

admin.site.register(Comparacion)