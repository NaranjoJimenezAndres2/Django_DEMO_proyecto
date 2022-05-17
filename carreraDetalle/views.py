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

def carreras(request,year,race,driverId):
    #pasar a int el valor year
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
    "$match":{"circuitName": race}
},
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
        "positionOrder":"$circuitResult.position",
        "points":"$circuitResult.points",
        "laps":"$circuitResult.laps",
        "time":"$circuitResult.time",
        "grid":"$circuitResult.grid",
        "fastestLap":"$circuitResult.fastestLap",
        "statusId":"$circuitResult.statusId"}
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
        "statusId":1,
        "constructorName":"$constructorDetail.name",
        "constructorNationality":"$constructorDetail.nationality"
    }
},
{
    "$match":{"driverId":driverId}
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
        "statusId":1,
        "constructorName":1,
        "constructorNationality":1,
        "code":"$driverDetail.code",
        "surname":"$driverDetail.surname",
        "forename":"$driverDetail.forename",
        "nationality":"$driverDetail.nationality"
    }
},
{
    "$lookup":{
        "localField":"statusId",
        "from":"status",
        "foreignField":"statusId",
        "as":"statusDetail"

    }
},
{
    "$unwind":"$statusDetail"
},
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
        "statusId":1,
        "constructorName":1,
        "constructorNationality":1,
        "code":1,
        "surname":1,
        "forename":1,
        "nationality":1,
        "status":"$statusDetail.status"}
},
{
    "$lookup":{
        "from": "lap_times",
        "let":{
            "driverId":"$driverId",
            "raceId": "$raceId",
            "laps":"$fastestLap"
        },
        "pipeline":[
            {
                "$match":{
                    "$expr":{
                        "$and":[
                            {
                                "$eq":["$driverId","$$driverId"]
                            },
                            {
                                "$eq":["$raceId","$$raceId"]
                            },
                            {
                                "$eq":["$lap","$$laps"]
                            },
                        ]
                    }
                }
            }
        ],
        "as":"fastestLapDetail"
    }
},
{
    "$unwind":"$fastestLapDetail"
},
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
        "statusId":1,
        "constructorName":1,
        "constructorNationality":1,
        "code":1,
        "surname":1,
        "forename":1,
        "nationality":1,
        "status":1,
        "lapFast": "$fastestLapDetail.time"
    }
}

]
    registros=collection.aggregate(pipeline)
    registros_df=pd.DataFrame(list(registros))
    #contatenar los campos forename y surname del dataframe registros_df
    registros_df['name']=pd.concat([registros_df['forename'],registros_df['surname']],axis=1).apply(lambda x: ' '.join(x),axis=1)
    #eliminar los campos forename y surname del dataframe registros_df
    registros_df.drop(['forename','surname'],axis=1,inplace=True)
    registros_df.drop(['raceId','_id','circuitId','constructorId','driverId'],axis=1,inplace=True)
    #generar el campo overtake para el dataframe registros_df restando grid y position
    registros_df['overtake']=registros_df['grid']-registros_df['positionOrder']
    
    #cambiar todos los valores NaN por 0
    registros_df.fillna(0,inplace=True)
    
    
    # mostrar el dataframe en el template como tabla
    #emision=registros_df.to_html(classes='table table-striped table-bordered table-hover')
    #return HttpResponse(emision)
    
    #enviar el dataframe como json
    return JsonResponse(registros_df.to_dict(orient='records'),safe=False)