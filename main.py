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

d = st.sidebar.text_input("Adresse de depart", 'Pontivy, France')
a = st.sidebar.text_input("Adresse d'arrivee", 'Rennes, France')


if (d != '') and (a != ''):
    location = geolocator.geocode(d)
    location1 = geolocator.geocode(a)
    lat0, lat1, lon0, lon1 = location.latitude, location1.latitude, location.longitude, location1.longitude
    data = {"lat": [lat0,lat1], "lon": [lon0, lon1]}
    df = pd.DataFrame(data)
    st.map(df)


req = 'http://router.project-osrm.org/route/v1/driving/'+str(lon0)+','+str(lat0)+';'+str(lon1)+','+str(lat1)
req += '?overview=full&geometries=geojson'

print(req)
rep = requests.get(req).json()
print(rep)

print(lat0,lat1)
print(lon0,lon1)
points =rep['routes'][0]['geometry']['coordinates']
print(points[:10])

X = [i[0] for i in points]
Y = [i[1] for i in points]

#print(X)
data0 = {"lat": Y, "lon": X}
df = pd.DataFrame(data0)
st.map(df)


