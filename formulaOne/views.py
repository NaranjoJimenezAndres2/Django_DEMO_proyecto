from this import d
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Comparacion
from .serializers import ComparacionSerializer
from django.conf import settings

# Create your views here.
import pymongo
import matplotlib.pyplot as plt
import matplotlib as pl
import numpy as np
import pandas as pd
import urllib , base64
import io
from matplotlib import style







    #emision=carreras_df.to_html(classes='table table-striped table-bordered table-hover')
    #return HttpResponse(emision)



@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])

def comparaciones(request, year, piloto1, piloto2):
    client= pymongo.MongoClient(settings.MONGO_URI)
    db = client.get_database('proyecto')  # obtenemos la base de datos
    collection = db.get_collection('races')
    pipeline = [{"$match":{
        "year": year
        }
    },
    {
        "$lookup":{
            "localField":"raceId",
            "from":"driver_standings",
            "foreignField":"raceId",
            "as":"driverStandings"

        }
    },
    {"$unwind":"$driverStandings"},
    {
        "$project":{
            "raceId":1,
            "year":1,
            "name":1,
            "date":1,
            "driverId": "$driverStandings.driverId",
            "points": "$driverStandings.points",
            "position": "$driverStandings.position",
            "wins": "$driverStandings.wins",

        }
    },
    {
        "$lookup":{
            "localField":"driverId",
            "from":"drivers",
            "foreignField":"driverId",
            "as":"driver"
        }
    },
    {"$unwind":"$driver"},
    {
        "$project":{
            "raceId":1,
            "year":1,
            "name":1,
            "date":1,
            "driverId":1,
            "points":1,
            "position":1,
            "wins":1,
            "code": "$driver.code",
            "surname": "$driver.surname",
        }
    },
    {
        "$lookup":{
            "localField":"driverId",
            "from": "qualifyings",
            "foreignField":"driverId",
            "as":"qualifying"
        }
    },
    {
        "$project":{
            "raceId":1,
            "year":1,
            "name":1,
            "date":1,
            "driverId":1,
            "points":1,
            "position":1,
            "wins":1,
            "code":1,
            "surname":1,
            
        }
    }
    ]
    carreras=collection.aggregate(pipeline)
    carreras_df=pd.DataFrame(list(carreras))
    # restar la posicion de los pilotos dentro del dataframe
    carreras_df['position']=carreras_df['position'].astype(int)
    carreras_df['points']=carreras_df['points'].astype(int)
    
    carreras_df=carreras_df[['name','date','code','surname','points']]
    
    carreras_df['date']=pd.to_datetime(carreras_df['date'])
    carreras_df=carreras_df.sort_values(by=['points'])
    carreras_df=carreras_df.reset_index(drop=True)
    
    carreras_df['nameSht']=carreras_df['name'].str.slice(0,3)
    
    
    piloto1_df=carreras_df[carreras_df['code'] == piloto1 ]
    piloto2_df=carreras_df[carreras_df['code'] == piloto2 ]
    
    
    pl.use('Agg')
    plt.figure(figsize=(10,5)) #tamaño de la figura
    plt.style.use('dark_background')
    plt.plot(piloto1_df['nameSht'] ,piloto1_df['points'],'o-g',  label= piloto1)
    plt.plot(piloto1_df['nameSht'] ,piloto2_df['points'],'*--',  label= piloto2)
    plt.legend()
    plt.xlabel('Grand Premio')
    plt.ylabel('Puntos')
    plt.title('Puntos en el campeonato')
    #plt.show()
    
    
    
    # devolver la grafica y los datos al html
    #return render(request, 'comparacion.html', )
    
    response = HttpResponse(content_type='image/png')
    plt.savefig(response, format='png')
    
    #devolver la url de la imagen
    return response

    



    #emision=piloto2_df.to_html(classes='table table-striped table-bordered table-hover')
    #return HttpResponse(emision)

    
     