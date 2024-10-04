# Import the libraries:

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from io import StringIO
from sklearn.metrics.pairwise import haversine_distances
from math import radians
from geopy.geocoders import Nominatim

import pandas as pd
import json
import datetime
import streamlit as st 

#Pick the file use to obtain the data
url = "https://www.data.gouv.fr/fr/datasets/r/fd54f81f-4389-4e73-be75-491133d011c3"
data = ""
data_times = ""
data_t = ""
resp = urlopen(url)
myzip = ZipFile(BytesIO(resp.read()))
filenames = myzip.namelist()

# Pick the dataset who concern the stops and the shedule
for line in myzip.open('stops.txt').readlines():
    data += line.decode('utf-8')
for line in myzip.open('stop_times.txt').readlines():
    data_times += line.decode('utf - 8') 

#Convert into a dataframe for both
data0 =StringIO(data)
data0_times =StringIO(data_times)

df = pd.read_csv(data0, sep=",")
df_trips = pd.read_csv(data0_times, sep=",")

# Show the dataframes
df
df_trips

def harversine_bus(x, y):
    departure_lat = df["stop_lat"]
    departure_lon = df["stop_lon"]
    min_d = 9999
    code_name_station = ""
    code_station = ""
    for item in range(len(departure_lat)):
        d = (x - departure_lat[item])*(x - departure_lat[item]) + (y - departure_lon[item])*(y - departure_lon[item])
        if d < min_d : 
            min_d = d
            code_name_station = df["stop_name"][item]
            code_station = df["stop_id"][item]
    return min_d, code_name_station, code_station

# User choice for the departure and the arrival for their travel
geolocator = Nominatim(user_agent="https://nominatim.openstreetmap.org/ui/search.html")

location_departure = st.text_input("Adress_departure")
location = geolocator.geocode(location_departure)
print((location.latitude, location.longitude))
test_harver, code_name_station, code_station = harversine_bus(location.latitude, location.longitude)
print("Departure shedule station : ", test_harver, code_name_station, code_station)

location_arrival = st.text_input("Adress Arrival")
location_arrival= geolocator.geocode(location_arrival)
print(location_arrival.latitude, location_arrival.longitude)

test_harver2, code_name_station, code_station = harversine_bus(location_arrival.latitude, location_arrival.longitude)
print("Arrival shedule station: ", test_harver2, code_name_station, code_station)

# User choice for the date and the hour 
d = st.date_input("Set your date ")
st.write("Your travel is set to", d)
t = st.time_input("Set a hour of departure for", value=None)
st.write("The hour of departure is set to", t)

def shedule_bus(code_station, starter_time):
    #departure_shedule = df_trips["stop_id"]
    departure_times = df_trips[df_trips["stop_id"] == code_station]
    secondes = int(starter_time[:2])*3600+ int(starter_time[3:5])*60+ int(starter_time[6:8])
    print(secondes)
    min_times = 9999
    dep = ""
    for item in departure_times["departure_time"]:
        secondes2 = int(item[:2])*3600+ int(item[3:5])*60+ int(item[6:8])
        secondes_diff = secondes2 - secondes
        if secondes_diff < min_times and secondes_diff >= 0:
            min_times = secondes_diff
            dep = item
    return dep, min_times

print(shedule_bus(code_station, str(t)))
