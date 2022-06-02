from this import d
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
# Create your views here.

import matplotlib as pl

from pprint import pprint
import bson

import fastf1 as ff1
import fastf1.plotting
import fastf1.legacy

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

import urllib , base64
import io
from matplotlib import style

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])

def estrategia(request,piloto1,gp,year):
    fastf1.plotting.setup_mpl()
    fastf1.Cache.enable_cache('cache') 
    
    year = int(year)
    
    
    race = ff1.get_session(year, gp, 'R')
    laps = race.load_laps(with_telemetry=True)
    
    
    driver_stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(
    ['Driver', 'Stint', 'Compound']
    ).count().reset_index()
    
    driver_stints_df = pd.DataFrame(driver_stints)
    
    driver_stints_df = driver_stints_df.rename(columns={'LapNumber': 'StintLength'})

    driver_stints_df = driver_stints_df.sort_values(by=['Stint'])
    
    # I only need ALO in driver_stints dataframe
    
    driver_stints_df = driver_stints_df[driver_stints_df['Driver'] == piloto1]
    
    # send data to the frontend
    
    json_data = driver_stints_df.to_dict( orient='records')
    
    return JsonResponse(json_data, safe=False)
    
    
    
    

