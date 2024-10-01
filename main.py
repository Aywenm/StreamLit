# environnement virtuel : dataIA

from urllib import request
import streamlit as st 
import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
import os

st.title('Mobility App')
st.sidebar.title('Rechercher un itinéraire')
geolocator = Nominatim(user_agent="https://nominatim.openstreetmap.org/ui/search.html")

d = st.sidebar.text_input("Adresse de depart", 'Pontivy')
a = st.sidebar.text_input("Adresse d'arrivee", 'Marseille')


if (d != '') and (a != ''):
    location = geolocator.geocode(d)
    location1 = geolocator.geocode(a)
    lat0, lat1, lon0, lon1 = location.latitude, location1.latitude, location.longitude, location1.longitude
    data = {"lat": [lat0,lat1], "lon": [lon0, lon1]}
    df = pd.DataFrame(data)
    st.map(df)

rep = requests.get('http://router.project-osrm.org/route/v1/driving/'+str(lat0)+','+str(lon0)+';'+str(lat1)+','+str(lon1)+'?overview=full&geometries=geojson').json()

print(rep)
#points =rep['routes'][0]['geometry']['coordinates']
#
#X = points[:][0]
#Y = points[0][:]
#np.array(points)
#print(X)


# X = [i[0] for i in points]
# Y = [i[1] for i in points]

# data0 = {"lat": X, "lon": Y}
# df = pd.DataFrame(data0)
# st.map(df)
