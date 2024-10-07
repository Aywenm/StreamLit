import streamlit as st
import openrouteservice
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests
import pandas
from css import add_custom_css

add_custom_css()
headers = {
    'API-Key': 'your api key',
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.get(
    'https://api.airfranceklm.com/opendata/flightstatus?startRange=2024-12-31T09:00:00Z&endRange=2024-12-31T23:59:59Z',
    headers=headers,
)



# Interface utilisateur
st.sidebar.markdown('<h1 class="main-title">Avion</h1>', unsafe_allow_html=True)

# vérifier si la requete a réussi
if response.status_code == 200:
    data = response.json()
else:
    print("Erreur lors de la requete:", response.status_code)


# Extraire toutes les villes de départ et d'arrivée
villes_depart = set()
villes_arrivee = set()

for flight in data['operationalFlights']:
    for flight_leg in flight['flightLegs']:
        villes_depart.add(flight_leg['departureInformation']['airport']['city']['name'])
        villes_arrivee.add(flight_leg['arrivalInformation']['airport']['city']['name'])

villes_depart = list(villes_depart)
villes_arrivee = list(villes_arrivee)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

with st.sidebar:
    from_address_input = st.selectbox(
        "Adresse de départ", villes_depart,
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="adresse de départ",
    )
    to_address_input = st.selectbox(
        "Adresse d'arrivée", villes_arrivee,
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="adresse d'arrivée",
    )


                
if st.sidebar.button('Calculer le trajet'):
    # Trouver le vol correspondant
    for flight in data['operationalFlights']:
        for flight_leg in flight['flightLegs']:
            if (flight_leg['departureInformation']['airport']['city']['name'] == from_address_input and
                flight_leg['arrivalInformation']['airport']['city']['name'] == to_address_input):
                status = flight_leg['statusName']
                départ_time = flight_leg['departureInformation']['times']['scheduled']
                arrivée_time = flight_leg['arrivalInformation']['times']['scheduled']
                st.sidebar.write('<h1 class="main-title">Calcul du trajet en avion</h1>', unsafe_allow_html=True)
                st.sidebar.write(f'<p class="duration">Trajet de {from_address_input} à {to_address_input}</p>', unsafe_allow_html=True)
                st.sidebar.write(f'<p class="duration">Date de départ : {départ_time}</p>', unsafe_allow_html=True)
                st.sidebar.write(f'<p class="duration">Date d arrivée : {arrivée_time}</p>', unsafe_allow_html=True)
                st.sidebar.write(f'<p class="duration">Statut du vol : {status}</p>', unsafe_allow_html=True)
               
                # Afficher les coordonnées de départ et d'arrivée
                départ_longitude = flight_leg['departureInformation']['airport']['location']['longitude']
                départ_latitude = flight_leg['departureInformation']['airport']['location']['latitude']
                arrivée_longitude = flight_leg['arrivalInformation']['airport']['location']['longitude']
                arrivée_latitude = flight_leg['arrivalInformation']['airport']['location']['latitude']

                # Créer une carte Folium
                m = folium.Map(location=[(départ_latitude + arrivée_latitude) / 2, (départ_longitude + arrivée_longitude) / 2], zoom_start=3)

                folium.plugins.Fullscreen(
                position="topright",
                title="Expand me",
                title_cancel="Exit me",
                force_separate_button=True,
                ).add_to(m)
                # Ajouter des marqueurs pour les aéroports de départ et d'arrivée
                folium.Marker([départ_latitude, départ_longitude], tooltip='Départ').add_to(m)
                folium.Marker([arrivée_latitude, arrivée_longitude], tooltip='Arrivée').add_to(m)

                # Ajouter une ligne entre les deux aéroports
                coordinates = [(départ_latitude, départ_longitude), (arrivée_latitude, arrivée_longitude)]
                folium.PolyLine(coordinates, color='blue').add_to(m)

            
                # Afficher la carte dans Streamlit
                folium_static(m)
                
                break
