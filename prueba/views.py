import re
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


from django.conf import settings

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def map(request, id):
    # declaramos la conexion en settings
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client.get_database('proyecto')  # obtenemos la base de datos
    collection = db.get_collection('races')
    pipeline = [
        {"$match": {
            "year": id
            }
        },
        {"$lookup": {
            "localField": "circuitId",
            "from": "circuits",
            "foreignField": "circuitId",
            "as": "union"
            }
        },
        {"$unwind": "$union"},
        {"$project": {
            "year": 1,
            "name": "$union.name",
            "lat": "$union.lat",
            "lng": "$union.lng"
            }
        }
    ]
    circuitos = collection.aggregate(pipeline)
    circuit_df = pd.DataFrame(list(circuitos))

    circuit_df['lat'] = circuit_df['lat'].astype(float)
    circuit_df['lng'] = circuit_df['lng'].astype(float)

    coordinates = []
    for lat, lng in zip(circuit_df['lat'], circuit_df['lng']):
        coordinates.append([lat, lng])
        maps = folium.Map(zoom_start=1, tiles='Stamen Toner')
    for i, j in zip(coordinates, circuit_df.name):
        marker = folium.Marker(location=i, icon=folium.Icon(icon='star', color='red'),
        popup="<strong>{0}</strong>".format(j))  # strong is used to bold the font (optional)
        marker.add_to(maps)

    maps = maps._repr_html_()
    id= id
    # maps.save('templates/map.html')
    # return render(request, 'map.html')
    # Display the map
    return render(request, 'map.html', {"maps":maps, 'id': id}) #parametros que se envian al html
