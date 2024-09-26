import folium
import pandas as pd
import requests
import streamlit as st  # Voor Streamlit functionaliteit
from streamlit_folium import st_folium  # Voor het renderen van de folium kaart

# Titel van de applicatie
st.title("Stemmen in Amsterdam per Stadsdeel")

# Beschrijving
st.write("""
Deze kaart toont de verdeling van stemmen op de vijf grootste politieke partijen per stadsdeel in Amsterdam.
""")

# Data voor het aantal stemmen per partij in elk stadsdeel (zonder tekst tussen haakjes)
stadsdeel_data = pd.DataFrame({
    'Stadsdeel': ['Centrum', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noord', 'Nieuw-West'],
    'VVD': [6925, 7054, 19318, 3347, 7315, 4576, 6910],
    'D66': [15804, 17686, 26210, 4297, 18430, 7465, 9757],
    'PVV': [1789, 2232, 5667, 1866, 2128, 4492, 4006],  # Alleen PVV, geen extra tekst
    'CDA': [1144, 1128, 4112, 732, 1243, 1028, 1428],
    'SP': [2481, 2876, 5387, 2226, 2897, 2725, 2886],  # Alleen SP, geen extra tekst
    'Total Votes': [56596, 67786, 106662, 33351, 70863, 45085, 60317]  # Totaal aantal stemmen per stadsdeel
})

# Bereken de percentages per partij
for partij in ['VVD', 'D66', 'PVV', 'CDA', 'SP']:  # Kolommen zonder extra tekst
    stadsdeel_data[partij + ' %'] = (stadsdeel_data[partij] / stadsdeel_data['Total Votes']) * 100

# Coördinaten van de stadsdelen (centroiden)
stadsdeel_coords = {
    'Centrum': [52.3728, 4.8936],
    'West': [52.3792, 4.8654],
    'Zuid': [52.3383, 4.8720],
    'Zuidoost': [52.3070, 4.9725],
    'Oost': [52.3625, 4.9415],
    'Noord': [52.4009, 4.9163],
    'Nieuw-West': [52.3600, 4.8103]
}

# Download de GeoJSON met stadsdeel grenzen
geojson_url = 'https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=INDELING_STADSDEEL&THEMA=gebiedsindeling'
response = requests.get(geojson_url)
geojson_data = response.json()

# Initialise de folium kaart gecentreerd op Amsterdam
amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=11)

# Voeg de GeoJSON laag toe met stadsdelen
folium.GeoJson(geojson_data, name="Stadsdelen").add_to(amsterdam_map)

# Voeg markers en pop-ups toe met de top 5 partijen per stadsdeel (in percentages)
for index, row in stadsdeel_data.iterrows():
    # Pop-up tekst met grotere lettergrootte en bold stijl (zonder haakjes)
    popup_text = f"""
    <div style="font-size: 14pt;">
    <b>{row['Stadsdeel']}</b><br>
    VVD: {row['VVD %']:.2f}%<br>
    D66: {row['D66 %']:.2f}%<br>
    PVV: {row['PVV %']:.2f}%<br>
    CDA: {row['CDA %']:.2f}%<br>
    SP: {row['SP %']:.2f}%<br>
    </div>
    """
    
    # Verkrijg de coördinaten voor het huidige stadsdeel
    coords = stadsdeel_coords.get(row['Stadsdeel'], [52.3676, 4.9041])  # Standaard coördinaten indien niet gevonden
    
    # Voeg een marker toe met de grotere pop-up
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_text, max_width=300)  # Vergroot de breedte van de pop-up
    ).add_to(amsterdam_map)

# Toon de kaart in Streamlit
st_folium(amsterdam_map, width=725)

