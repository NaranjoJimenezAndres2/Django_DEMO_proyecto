from django.shortcuts import render



import re
from this import d
from xmlrpc.client import TRANSPORT_ERROR
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


from django.conf import settings


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

def getpilotos(request, year):
    client= pymongo.MongoClient(settings.MONGO_URI)
    db = client.get_database('proyecto')
    collection = db.get_collection('races')
    pipeline = [{"$match":{
        "year":year
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
            "_id":0,
            "code": "$driver.code",
            "surname": "$driver.surname",
            "forename": "$driver.forename",
        }
    },
    ]
    pilotos=collection.aggregate(pipeline)
    pilotos_df=pd.DataFrame(list(pilotos))
    
    #eliminar duplicados con el mismo "code"
    pilotos_df=pilotos_df.drop_duplicates(subset=['code'], keep='first')
    
    return JsonResponse(pilotos_df.to_dict(orient='records'),safe=False)
