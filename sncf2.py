import streamlit as st
import pandas as pd
import numpy as np
import requests
from geopy.distance import distance
import folium
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


st.set_page_config(layout='wide')
page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)
page_height = streamlit_js_eval(js_expressions='window.parent.innerHeight', key='HEIGHT',  want_output = True,)

url0 = 'https://api.sncf.com/v1/coverage/sncf/'
SNCF_API_KEY = "c6abef60-03b3-4e1c-90c9-275e9c168fdb"
headers = {'Authorization': SNCF_API_KEY}

def getDateAndTime(dt):
    year = dt[:4]
    month = dt[4:6]
    day = dt[6:8]
    hour = dt[9:11]
    min = dt[11:13]
    sec = dt[13:15]
    return day+'/'+month+'/'+year+' '+hour+':'+min

def get_train_route(start_coords, end_coords):
    url = f"{url0}journeys?from={start_coords[1]};{start_coords[0]}&to={end_coords[1]};{end_coords[0]}"
    url += "&free_radius_from=500000&free_radius_to=50000"
    url += "&mode=networks"
    # url += "&datetime=20241002T160440"
    url += "&max_duration_to_pt=3600"
    response = requests.get(url, headers=headers)
    print(url)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f)
    return response.json()

#brest
lat0 = 48.389870
lon0 = -4.487180

#marseille
lat1 = 43.296482
lon1 = 5.369780

start_coords = [lat0, lon0]
end_coords = [lat1, lon1]
print('start : ',start_coords)
print('end : ',end_coords)

test = get_train_route(start_coords, end_coords)
print(test)
points = []
mainpoints = []
mainnames = []

m = folium.Map(location = start_coords, width=page_width, height = page_height/1.5)

if not 'error' in test:
    route = test['journeys'][0]
    dtime = route['departure_date_time']
    atime = route['arrival_date_time']
    if 'sections' in route:
        journey = route['sections']
        for section in journey:
            if 'type' in section:
                if section['type'] == 'crow_fly':
                    if 'geojson' in section:
                        for coords in section['geojson']['coordinates']:
                            print('crow fly : ',coords)
                            folium.CircleMarker([coords[1],coords[0]], radius = 5, color ='green', weight=1, fill_opacity=0.5, fill_color='green').add_to(m)
                if section['type'] == 'public_transport':
                    dtime0 = section['departure_date_time']
                    atime0 = section['arrival_date_time']
                    if 'geojson' in section:
                        for i in range(len(section['geojson']['coordinates'])):
                            coords = section['geojson']['coordinates'][i]
                            text = section['display_informations']['network']
                            folium.CircleMarker([coords[1],coords[0]], radius = 10, color ='yellow', weight=1, fill_opacity=0.5, fill_color='yellow', tooltip=text).add_to(m)
                if section['type'] == 'transfert':
                    if 'geojson' in section:
                        for coords in section['geojson']['coordinates']:
                            folium.CircleMarker([coords[1],coords[0]], radius = 20, color ='black', weight=1, fill_opacity=0.5, fill_color='black').add_to(m)

print('nb de points : ',len(points))
print('heure de depart : ',dtime)
print('heure d''arrivee : ',atime)
getDateAndTime(dtime)

folium.Marker(start_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip=getDateAndTime(dtime)).add_to(m)
folium.Marker(end_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip=getDateAndTime(atime)).add_to(m)

st.components.v1.html(folium.Figure().add_child(m).render(), width=page_width, height=1500)

