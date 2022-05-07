from this import d
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
# Create your views here.
import pymongo
import pandas as pd
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



def telemetria(request):
    fastf1.plotting.setup_mpl()
    fastf1.Cache.enable_cache('cache') 


    race = fastf1.get_session(2020, 'Turkish Grand Prix', 'R')
    race.load()

    lec = race.laps.pick_driver('LEC')
    ham = race.laps.pick_driver('HAM')

    fig, ax = plt.subplots()
    ax.plot(lec['LapNumber'], lec['LapTime'], color='red')
    ax.plot(ham['LapNumber'], ham['LapTime'], color='cyan')
    ax.set_title("LEC vs HAM")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
     # convertir el grafico a una imagen
     
     
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string= base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    # devolver la grafica y los datos al html
    return render(request, 'comparacion.html', {'data':uri})
    
    
       