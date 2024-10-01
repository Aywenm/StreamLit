from urllib import request
import streamlit as st 
import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim




geolocator = Nominatim(user_agent="https://nominatim.openstreetmap.org/ui/search.html")

text_location_departure = st.text_input("Adress_departure")
location = geolocator.geocode(text_location_departure)
text_location_arrival = st.text_input("Adress_arrival")
location1 = geolocator.geocode(text_location_arrival)


print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
data = {"lat": [location.latitude, location1.latitude], "lon": [location.longitude, location1.longitude]}
df = pd.DataFrame(data)
st.map(df)

# https://valhalla1.openstreetmap.de/route?json={%22costing%22:%22auto%22,%22exclude_polygons%22:[],%22locations%22:[{%22lon%22:-2.6819,%22lat%22:48.4882,%22type%22:%22break%22},{%22lon%22:2.3484,%22lat%22:48.8535,%22type%22:%22break%22}],%22directions_options%22:{%22units%22:%22kilometers%22},%22id%22:%22valhalla_directions%22}
