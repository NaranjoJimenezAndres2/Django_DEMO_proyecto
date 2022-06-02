"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from urllib.parse import parse_qs
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

#Aqui se enrutan las urls de la aplicacion

urlpatterns = [
    #path('formulaOne/', include('formulaOne.urls')), #Aqui se enruta la aplicacion formulaOne a la url formulaOne capturando todas las urls de la aplicacion urls.py
    path('admin/', admin.site.urls),
    path ('', include('formulaOne.urls')),#al estar vacio puedes poner directamente el segundo parametro que esta dentro de la aplicacion
    path ('', include('prueba.urls')),
    path ('', include('comparacionDjango.urls')),
    path ('', include('mostrarCarrera.urls')),
    path ('', include('carreraDetalle.urls')),
    path ('', include('telemetria.urls')),
    path ('', include('getPilotos.urls')),
    path ('', include('estrategia.urls')),
    path ('', include('telemetriaOne.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
