from django.shortcuts import render
from this import d
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
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
# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
#hacer una comparacion entre dos dataframes y devolver una grafica. Los datos estan filtrados por el año 2021 y se compararan los datos de dos pilotos. Los datos estan extraidos de MongoDB
def comparacion(request, year, piloto1, piloto2):
    plt.close()
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
    

    
    plt.style.use('dark_background')
    plt.plot(piloto1_df['nameSht'] ,piloto1_df['points'],'o-g',  label= piloto1)
    plt.plot(piloto1_df['nameSht'] ,piloto2_df['points'],'*--',  label= piloto2)
    plt.legend()
    plt.xlabel('Grand Premio')
    plt.ylabel('Puntos')
    plt.title('Puntos en el campeonato')
    # convertir el grafico a una imagen
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string= base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    # devolver la grafica y los datos al html
    return render(request, 'comparacion.html', {'data':uri})
    



    #emision=carreras_df.to_html(classes='table table-striped table-bordered table-hover')
    #return HttpResponse(emision)
