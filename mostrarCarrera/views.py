import re
from this import d
from xmlrpc.client import TRANSPORT_ERROR
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

def carreras(request, year, nombreCircuito):
    year = int(year)
    client= pymongo.MongoClient(settings.MONGO_URI)
    db = client.get_database('proyecto')
    collection = db.get_collection('races')
    pipeline = [{"$match":{
    "year": year
    }
},
{
    "$lookup":{
        "localField":"circuitId",
        "from":"circuits",
        "foreignField":"circuitId",
        "as":"circuitDetail"

    }
},
{"$unwind":"$circuitDetail"},
{
    "$project":{
        "raceId":1,
        "name":1,
        "date":1,
        "circuitId":"$circuitDetail.circuitId",
        "circuitName":"$circuitDetail.name",
    }
},
{
    "$match":{"circuitName":nombreCircuito},
}
,
{
    "$lookup":{
        "localField":"raceId",
        "from":"results",
        "foreignField":"raceId",
        "as":"circuitResult"

    }
},
{"$unwind":"$circuitResult"},
{
    "$project":{
        "raceId":1,
        "name":1,
        "date":1,
        "circuitId":1,
        "circuitName":1,
        "driverId":"$circuitResult.driverId",
        "constructorId":"$circuitResult.constructorId",
        "number":"$circuitResult.number",
        "positionOrder":"$circuitResult.positionOrder",
        "points":"$circuitResult.points",
        "laps":"$circuitResult.laps",
        "time":"$circuitResult.time",
        "grid":"$circuitResult.grid",
        "fastestLap":"$circuitResult.fastestLap",
        "status":"$circuitResult.status"}
},
{
    "$lookup":{
        "localField":"constructorId",
        "from":"constructors",
        "foreignField":"constructorId",
        "as":"constructorDetail"

    }
},
{"$unwind":"$constructorDetail"},
{
    "$project":{
        "raceId":1,
        "name":1,
        "date":1,
        "circuitId":1,
        "circuitName":1,
        "driverId":1,
        "constructorId":1,
        "number":1,
        "positionOrder":1,
        "points":1,
        "laps":1,
        "time":1,
        "grid":1,
        "fastestLap":1,
        "status":1,
        "constructorName":"$constructorDetail.name",
        "constructorNationality":"$constructorDetail.nationality"
    }
},
{
    "$lookup":{
        "localField":"driverId",
        "from":"drivers",
        "foreignField":"driverId",
        "as":"driverDetail"

    }
},
{"$unwind":"$driverDetail"},
{
    "$project":{
        "raceId":1,
        "name":1,
        "date":1,
        "circuitId":1,
        "circuitName":1,
        "driverId":1,
        "constructorId":1,
        "number":1,
        "positionOrder":1,
        "points":1,
        "laps":1,
        "time":1,
        "grid":1,
        "fastestLap":1,
        "status":1,
        "constructorName":1,
        "constructorNationality":1,
        "code":"$driverDetail.code",
        "forename":"$driverDetail.forename",
        "surname":"$driverDetail.surname",
        "nationality":"$driverDetail.nationality"
    }
}]
    registros=collection.aggregate(pipeline)
    registros_df=pd.DataFrame(list(registros))
    #contatenar los campos forename y surname del dataframe registros_df
    registros_df['name']=pd.concat([registros_df['forename'],registros_df['surname']],axis=1).apply(lambda x: ' '.join(x),axis=1)
    #eliminar los campos forename y surname del dataframe registros_df
    registros_df.drop(['forename','surname'],axis=1,inplace=True)
    registros_df.drop(['raceId','_id','circuitId','constructorId'],axis=1,inplace=True)
    #cambiar el valor /N de time por string --
    registros_df=registros_df.replace(to_replace=r'\N',value='--',regex=True)
    #pasar el campo puntos a int.
    registros_df['position']=registros_df['position'].astype(int)
    #ordenar el dataframe por puntos
    registros_df.sort_values(by=['positionOrder'],ascending=True,inplace=True)
    
    
    # mostrar el dataframe en el template como tabla
    #emision=registros_df.to_html(classes='table table-striped table-bordered table-hover')
    #return HttpResponse(emision)
    
    #enviar el dataframe como json
    return JsonResponse(registros_df.to_dict(orient='records'),safe=False)
    
    
    

    
    