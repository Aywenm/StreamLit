import streamlit as st
import openrouteservice
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests
import pandas
from css import add_custom_css

add_custom_css()

# Interface utilisateur
st.sidebar.markdown('<h1 class="main-title">maps</h1>', unsafe_allow_html=True)

# Configurer la clé API OpenRouteService
ORS_API_KEY = 'Your api key'# clé api open route service
client = openrouteservice.Client(key=ORS_API_KEY)# api open route service

# Fonction pour obtenir les informations de trajet
def get_route_info(from_address, to_address, mode):
    from_coords = client.pelias_search(from_address)['features'][0]['geometry']['coordinates']# recherche de l'adresse de départ
    to_coords = client.pelias_search(to_address)['features'][0]['geometry']['coordinates']# recherche de l'adresse d'arrivée

    # Afficher les coordonnées pour vérification
    st.sidebar.write(f"Coordonnées de départ: {from_coords}")# affichage des coordonnées de départ
    st.sidebar.write(f"Coordonnées d'arrivée: {to_coords}")# affichage des coordonnées d'arrivée
    
    modes = {
        'driving': 'driving-car',
        'walking': 'foot-walking',
        'bicycling': 'cycling-regular',
        'flash': 'foot-walking'
    }
    # Multiplier la vitesse par 2 pour le mode 'flash'
    if mode == 'flash':
        from_coords = client.pelias_search(from_address)['features'][0]['geometry']['coordinates']
        to_coords = client.pelias_search(to_address)['features'][0]['geometry']['coordinates']
        route = client.directions(coordinates=[from_coords, to_coords], profile=modes[mode], format='geojson')
        if route:
            duration = route['features'][0]['properties']['segments'][0]['duration'] / 60 /200000000
            distance = route['features'][0]['properties']['segments'][0]['distance'] / 1000
            duration = round(duration, 50)
            return duration, distance, route
    
    # Vérifier si le mode est valide
    if mode not in modes:
        return None
    route = client.directions(coordinates=[from_coords, to_coords], profile=modes[mode], format='geojson')  # Obtenir les informations de trajet
    if route:
        duration = route['features'][0]['properties']['segments'][0]['duration'] / 60  # Convertir en minutes
        distance = route['features'][0]['properties']['segments'][0]['distance'] / 1000  # Convertir en km
        return duration, distance, route
    else:
        return None

# Fonction pour afficher la carte avec le trajet
state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)
def display_route_map(route):
    # Extraire toutes les coordonnées du trajet
    coordinates = route['features'][0]['geometry']['coordinates']
    
    # Créer une carte centrée sur le point de départ
    m = folium.Map(location=[coordinates[0][1], coordinates[0][0]], zoom_start=8)
    
    
    
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)
    
    folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",).add_to(m)


    # Ajouter le trajet à la carte
    folium.GeoJson(route, name='route').add_to(m)
    
    # Ajuster le zoom pour inclure toutes les coordonnées du trajet
    m.fit_bounds([[coord[1], coord[0]] for coord in coordinates])
    
    folium.LayerControl().add_to(m)
    return m



# Vérifier si les variables de session existent
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "Adresse de départ"
# Interface utilisateur
with st.sidebar:
    from_address_input = st.text_input( # Ajouter une zone de texte pour l'adresse de départ
        "Adresse de départ",
        label_visibility=st.session_state.visibility, # Ajouter une option pour la visibilité de l'étiquette
        disabled=st.session_state.disabled,# Ajouter une option pour désactiver la zone de texte
        placeholder=st.session_state.placeholder,# Ajouter une option pour le texte d'aide
    )
    to_address_input = st.text_input(
        "Adresse d'arrivée",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="adresse d'arrivée",
    )
    mode = st.selectbox('Mode de transport', ['driving', 'walking', 'bicycling', 'flash'])# Ajouter une liste déroulante pour le mode de transport

# Vérifier si le bouton a été cliqué
if st.sidebar.button('Calculer le trajet'):
    duration, distance, route = get_route_info(from_address_input, to_address_input, mode)# Obtenir les informations de trajet
    if duration and distance and route:# Vérifier si les informations de trajet existent
        st.sidebar.markdown(f'<p class="duration">Durée: {duration:.5f} minutes</p>', unsafe_allow_html=True)
        st.sidebar.markdown(f'<p class="duration">Distance: {distance:.2f} km</p>', unsafe_allow_html=True)
        st.write(f"le moyen de transport selectionner est {mode}")
        route_map = display_route_map(route)# Afficher la carte avec le trajet
        folium_static(route_map)# Afficher la carte
    else:
        st.write('Impossible de calculer le trajet. Veuillez vérifier les adresses et réessayer.')
