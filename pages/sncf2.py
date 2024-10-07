import streamlit as st
import requests
from geopy.geocoders import Nominatim
import folium
import json
from css import add_custom_css
add_custom_css()
####################################################################################################################################

st.markdown(
    """
    <style>
    .duration {
        font-size: 1.2em;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)
geolocator = Nominatim(user_agent="mobility_app")
colors = ['orange', 'blue', 'lightred', 'pink', 'black', 'beige', 'gray', 'lightgreen', 'darkpurple', 'cadetblue', 
          'darkred', 'lightgray', 'white', 'purple', 'red', 'green', 'darkblue', 'darkgreen', 'lightblue']
phys_modes =[]
mainpoints = []
# mainnames = []
sectionNb = 0

####################################################################################################################################

def hashColor(s):
    if not s in phys_modes:
        phys_modes.append(s)
    return phys_modes.index(s)

def getDateAndTime(dt):
    year = dt[:4]
    month = dt[4:6]
    day = dt[6:8]
    hour = dt[9:11]
    min = dt[11:13]
    sec = dt[13:15]
    return day+'/'+month+'/'+year+' '+hour+':'+min

def get_train_route(start_coords, end_coords):
    url0 = 'https://api.sncf.com/v1/coverage/sncf/'
    SNCF_API_KEY = "your api key"
    headers = {'Authorization': SNCF_API_KEY}
    url = f"{url0}journeys?from={start_coords[1]};{start_coords[0]}&to={end_coords[1]};{end_coords[0]}"
    url += "&free_radius_from=100&free_radius_to=100"
    url += "&max_duration_to_pt=10000"
    #url += "&mode=networks"
    # url += "&datetime=20241002T160440"
    response = requests.get(url, headers=headers)
   
    return response.json()

####################################################################################################################################

# on prend 2 villes en entree, une de depart, et une d'arrivee
d = st.sidebar.text_input('Adresse de départ', 'Chateaulin, Finistère, France')
a = st.sidebar.text_input("Adresse d'arrivée", 'Vidauban, France')

# on convertit en coordonnées gps
loc0 = geolocator.geocode(d)
loc1 = geolocator.geocode(a)
lat0, lon0 = loc0.latitude, loc0.longitude
lat1, lon1 = loc1.latitude, loc1.longitude
start_coords = [lat0, lon0]
end_coords = [lat1, lon1]

# on envoie une requete GET pour avoir les informations d'itineraires
reponse_json = get_train_route(start_coords, end_coords)

# on prepare une carte du monde
m = folium.Map(location = start_coords, width = 800, height = 600)
folium.Marker(start_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip='DEPART').add_to(m)
folium.Marker(end_coords, radius = 20, color ='red', weight=1, fill_opacity=0.5, fill_color='red', tooltip='ARRIVEE').add_to(m)

# parsing de la reponse json
if not 'error' in reponse_json:
    journey = reponse_json['journeys'][0]
    dtime = journey['departure_date_time']
    atime = journey['arrival_date_time']
    if 'sections' in journey:
        for section in journey['sections']:
            dtimeSec = section['departure_date_time']
            atimeSec = section['arrival_date_time']
            type = section['type']
            
            # si le type de section est vol d'oiseau, marche de rue, correspondance, ce n'est pas un transport public
            if type in ['crow_fly','street_network','transfer']:
                if 'geojson' in section:
                    dest_type = section['to']['embedded_type']
                    if dest_type == 'stop_point':
                        st.sidebar.markdown(
                            f"<div class='duration'>{getDateAndTime(dtimeSec)}<br>Aller à la gare de : {section['to']['name']}</div>",
                            unsafe_allow_html=True
                        )
                    elif dest_type == 'address':   
                        st.sidebar.markdown(
                            f"<div class='duration'>{getDateAndTime(dtimeSec)}<br>Aller à : {section['to']['name']}<br>vous êtes arrivé</div>",
                            unsafe_allow_html=True
                        )
                    for coords in section['geojson']['coordinates']:
                        folium.CircleMarker([coords[1],coords[0]], radius = 5, color ='green', weight=1, 
                            fill_opacity=0.5, fill_color='green').add_to(m)
            
            # si le type de section est transport public, on precise le mode avec phys_mode (autocar, ter, rer, tgv)
            if type == 'public_transport':
                phys_mode = section['display_informations']['physical_mode']
                commercial_mode = section['display_informations']['network']
                col = colors[hashColor(phys_mode)]
                st.sidebar.text(getDateAndTime(dtimeSec)+'\nprendre : '+phys_mode+'\njusque '+ section['to']['name'])
                if 'geojson' in section:
                    poly = []
                    for coords in section['geojson']['coordinates']:
                        folium.CircleMarker([coords[1],coords[0]], radius = 15, color ='yellow', weight=1, 
                            fill_opacity=0.5, fill_color='yellow', tooltip=phys_mode).add_to(m)
                        folium.Marker([coords[1],coords[0]], icon=folium.Icon(color=col, icon='train', prefix='fa'),
                            tooltip=commercial_mode).add_to(m)
                        poly.append([coords[1],coords[0]])
                    sectionNb += 1
                    folium.PolyLine(locations=poly, color="gray", weight=5, tooltip="Section "+str(sectionNb)).add_to(m)
            
    st.sidebar.markdown(
        f"<div class='duration'>Départ : {getDateAndTime(dtime)}<br>Arrivée : {getDateAndTime(atime)}</div>",
        unsafe_allow_html=True
    )
 
st.components.v1.html(folium.Figure().add_child(m).render(), width=800, height=600)

