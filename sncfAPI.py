import streamlit as st
import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
from geopy.distance import distance
import folium
import json
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


st.set_page_config(layout='wide')
page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)
page_height = streamlit_js_eval(js_expressions='window.parent.innerHeight', key='HEIGHT',  want_output = True,)
# st.write(page_width)

url0 = 'https://api.sncf.com/v1/coverage/sncf/'
#url0 = 'https://api.sncf.com/v1/'
SNCF_API_KEY = "c6abef60-03b3-4e1c-90c9-275e9c168fdb"
headers = {'Authorization': SNCF_API_KEY}

def getDateAndTime(dt):
    year = dt[:4]
    month = dt[4:6]
    day = dt[6:8]
    hour = dt[9:11]
    min = dt[11:13]
    sec = dt[13:15]
#    print('date time : ',year,month,day,hour,min,sec)
    return day+'/'+month+'/'+year+' '+hour+':'+min

def get_train_route(start_coords, end_coords):
    url = f"{url0}journeys?from={start_coords[1]};{start_coords[0]}&to={end_coords[1]};{end_coords[0]}"
    url += "&free_radius_from=500000&free_radius_to=50000"
    url += "&mode=networks"
    # url += "&datetime=20241002T160440"
    url += "&max_duration_to_pt=3600"

    headers = {'Authorization': SNCF_API_KEY}
    response = requests.get(url, headers=headers)
    print(url)
    # print(f"Response Code: {response.status_code}")  # Log du code de réponse
    # print(f"Response Content: {response.content}") 
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f)
    return response.json()

geolocator = Nominatim(user_agent="mobility_app")

# d = 'Brest, France'
# a = 'Marseille, France'
# location = geolocator.geocode(d)
# location1 = geolocator.geocode(a)
# lat0, lon0 = location.latitude, location.longitude
# lat1, lon1 = location1.latitude, location1.longitude

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

# start_coords = [48.8964762, 2.551772]
# end_coords = [48.1113387, -1.6800198]

test = get_train_route(start_coords, end_coords)
print(test)
points = []
mainpoints = []
mainnames = []

m = folium.Map(location = start_coords, width=page_width, height = page_height/1.5)

# folium.CircleMarker(start_coords).add_to(m)
# folium.CircleMarker(end_coords).add_to(m)

# if not 'error' in test:
#     for route in test['journeys']:
#         if 'sections' in route:
#             journey = route['sections']
#             for coords in journey:
#                 if 'geojson' in coords:
#                     points.extend(coords['geojson']['coordinates'])

if not 'error' in test:
    route = test['journeys'][0]
    dtime = route['departure_date_time']
    atime = route['arrival_date_time']
    if 'sections' in route:
        journey = route['sections']
        for coords in journey:
            if 'type' in coords:
                if coords['type'] != 'crow_fly':
                    if 'geojson' in coords:
                        points.extend(coords['geojson']['coordinates'])
    if 'terminus' in test:
        for terminus in test['terminus']:
            mainpoints.append([float(terminus['coord']['lat']),float(terminus['coord']['lon'])])
            mainnames.append(terminus['label'])


print('terminus :\n')
print(mainnames)
print(mainpoints)

print('nb de points : ',len(points))
print('heure de depart : ',dtime)
print('heure d''arrivee : ',atime)
getDateAndTime(dtime)

folium.Marker(start_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip=getDateAndTime(dtime)).add_to(m)
folium.Marker(end_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip=getDateAndTime(atime)).add_to(m)

X = [i[0] for i in points]
Y = [i[1] for i in points]

# for p in points:
#     # print(p)
#     folium.CircleMarker([p[1],p[0]], radius = 15, color ='blue', weight=1, fill_opacity=0.5, fill_color='blue').add_to(m)

for p in range(len(mainpoints)):
    # print(p)
    folium.CircleMarker(mainpoints[p], radius = 15, color ='blue', weight=1, fill_opacity=0.5, fill_color='blue', tooltip=mainnames[p]).add_to(m)

st.components.v1.html(folium.Figure().add_child(m).render(), width=page_width, height=1500)


