from this import d
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
# Create your views here.
import pymongo
import pandas as pd
import matplotlib as pl
import numpy as np
import folium

from pprint import pprint
import bson

import fastf1 
import fastf1.plotting
import fastf1.legacy

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

import urllib , base64
import io
from matplotlib import style



def telemetria(request, piloto1, piloto2,gp, year):
    fastf1.plotting.setup_mpl()
    fastf1.Cache.enable_cache('cache') 

    year = int(year)

    race = fastf1.get_session(year, gp, 'R')
    race.load()

    lec = race.laps.pick_driver(piloto1)
    ham = race.laps.pick_driver(piloto2)


    pl.use('Agg')
    plt.figure(figsize=(10,5)) #tamaño de la figura
    plt.style.use('dark_background')
    
    plt.plot(lec['LapNumber'], lec['LapTime'],'o-g',  label= piloto1, color='red')
    plt.plot(ham['LapNumber'], ham['LapTime'],'*--',  label= piloto2, color='cyan')
    plt.title(piloto1 + ' vs ' + piloto2)
    plt.grid(color='w', linestyle='-', linewidth=0.5)
    plt.legend()
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time")
     # convertir el grafico a una imagen
     
     
    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    
    #devolver la url de la imagen
    return response
    
    
       