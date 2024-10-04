# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk
# from st_keyup import st_keyup

# @st.cache_data
# def from_data_file(filename):
#     url = (
#         "https://raw.githubusercontent.com/streamlit/"
#         "example-data/master/hello/v1/%s" % filename
#     )
#     return pd.read_json(url)



# try:
#     ALL_LAYERS = {
#         "Bike Rentals": pdk.Layer(
#             "HexagonLayer",
#             data=from_data_file("bike_rental_stats.json"),
#             get_position=["lon", "lat"],
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             extruded=True,
#         ),
#         "Bart Stop Exits": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_color=[200, 30, 0, 160],
#             get_radius="[exits]",
#             radius_scale=0.05,
#         ),
#         "Bart Stop Names": pdk.Layer(
#             "TextLayer",
#             data=from_data_file("bart_stop_stats.json"),
#             get_position=["lon", "lat"],
#             get_text="name",
#             get_color=[0, 0, 0, 200],
#             get_size=10,
#             get_alignment_baseline="'bottom'",
#         ),
#         "Outbound Flow": pdk.Layer(
#             "ArcLayer",
#             data=from_data_file("bart_path_stats.json"),
#             get_source_position=["lon", "lat"],
#             get_target_position=["lon2", "lat2"],
#             get_source_color=[200, 30, 0, 160],
#             get_target_color=[200, 30, 0, 160],
#             auto_highlight=True,
#             width_scale=0.0001,
#             get_width="outbound",
#             width_min_pixels=3,
#             width_max_pixels=30,
#         ),
#     }
#     st.sidebar.markdown("### Map Layers")
#     selected_layers = [
#         layer
#         for layer_name, layer in ALL_LAYERS.items()
#         if st.sidebar.checkbox(layer_name, True)
#     ]
#     if selected_layers:
#         st.pydeck_chart(
#             pdk.Deck(
#                 map_style=None,
#                 initial_view_state={
#                     "latitude": 37.76,
#                     "longitude": -122.4,
#                     "zoom": 11,
#                     "pitch": 50,
#                 },
#                 layers=selected_layers,
#             )
#         )
#     else:
#         st.error("Please choose at least one layer above.")
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )
    

from urllib import request
import streamlit as st
import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
import os
from css import add_custom_css
st.title('Mobility App')
st.sidebar.title('Rechercher un itinéraire')
add_custom_css()
geolocator = Nominatim(user_agent="mobility_app")

d = st.sidebar.text_input("Adresse de départ", 'Pontivy, France')
a = st.sidebar.text_input("Adresse d'arrivée", 'Rennes, France')

# Transport options
option = st.sidebar.selectbox("Transport", ("voiture", "vélos", "pied"), index=0)
st.write("Vous avez sélectionné:", option)

if d and a:
    location = geolocator.geocode(d)
    location1 = geolocator.geocode(a)
    lat0, lon0 = location.latitude, location.longitude
    lat1, lon1 = location1.latitude, location1.longitude

    data = {"lat": [lat0, lat1], "lon": [lon0, lon1]}
    df = pd.DataFrame(data)

    def get_route(option):
        if option == "voiture":
            req = f'http://router.project-osrm.org/route/v1/driving/{lon0},{lat0};{lon1},{lat1}?overview=full&geometries=geojson'
        elif option == "vélos":
            req = f'http://router.project-osrm.org/route/v1/bike/{lon0},{lat0};{lon1},{lat1}?overview=full&geometries=geojson'
        else: #option == "pied":
            req = f'http://router.project-osrm.org/route/v1/foot/{lon0},{lat0};{lon1},{lat1}?overview=full&geometries=geojson'
        return req

    req = get_route(option)
    rep = requests.get(req).json()
    print(req)
    rep = requests.get(req).json()
    print(rep)

    print(lat0,lat1)
    print(lon0,lon1)
    points =rep['routes'][0]['geometry']['coordinates']
    print(points[:10])
    duree =rep['routes'][0]['duration']
    dist =rep['routes'][0]['distance']
    print(duree,dist)
    duree_result=duree/60
    dist_result=dist/1000


    X = [i[0] for i in points]
    Y = [i[1] for i in points]

#print(X)
    data0 = {"lat": Y, "lon": X}
    df = pd.DataFrame(data0)
    st.map(df)
    st.write(f"En {option}, vous allez mettre {duree_result:.2f} min pour parcourir {dist_result:.2f} km.")
   
    
 