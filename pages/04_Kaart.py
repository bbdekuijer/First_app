import streamlit as st
import folium
from streamlit_folium import st_folium

# Coördinaten van de locaties
locations = {
    "Cherbourg (C)": [49.634, -1.621],
    "Queenstown (Q)": [51.841, -8.293],
    "Southampton (S)": [50.901, -1.404]
}

# Start Streamlit-app
st.title("Kaart met locaties van C, Q en S")

# Maak een kaart op een gemiddelde locatie tussen de drie punten
map_center = [51, -5]  # Gemiddeld punt tussen de locaties
map = folium.Map(location=map_center, zoom_start=5)

# Voeg markers toe voor elke locatie zonder HTML-formattering
for name, coords in locations.items():
    folium.Marker(
        location=coords,
        popup=name,  # Zonder HTML-formattering
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

# Toon de kaart in Streamlit
st_folium(map, width=700, height=500)
