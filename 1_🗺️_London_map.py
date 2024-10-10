import streamlit as st
import folium
import json
from streamlit_folium import st_folium


# Functie om een layer aan te maken voor een specifieke zone
def create_zone_layer(stations_data, zone, map_object, color):
    # Filter de stations voor de specifieke zone
    zone_layer = folium.FeatureGroup(name=f'Zone {zone}').add_to(map_object)
    
    for station in stations_data['features']:
        # Haal de zone van het station op
        station_zone = station['properties']['zone']
        
        # Voeg alleen stations toe die in de specifieke zone zitten
        if station_zone == zone:
            coords = station['geometry']['coordinates']
            name = station['properties']['name']
            marker_color = station['properties']['marker-color']
            
            # Voeg cirkelmarkeringen toe voor elk station in deze zone
            folium.Circle(
                location=[coords[1], coords[0]],  # Gebruik lat en lng
                popup=name,  # Laat de naam van het station zien
                tooltip=f"Station: {name}, Zone: {station_zone}",  # Toon station en zone in de tooltip
                color=marker_color,  # Gebruik de 'marker-color' als kleur voor de cirkel
                fill=True,
                fill_color=marker_color,  # Vulkleur gelijk aan de cirkelkleur
                fill_opacity=0.7,  # Vul de cirkel met transparantie
                radius=300  # Stel een vaste straal in
            ).add_to(zone_layer)
    
    return map_object

# Functie om een categorische legenda aan de kaart toe te voegen
def add_categorical_legend(map_object, title, colors, labels):
    legend_html = f'''
     <div style="position: fixed; 
     top: 10px; right: 10px; width: 150px; height: 180px; 
     background-color: white; z-index:9999; font-size:14px;
     padding: 10px;
     border: 2px solid grey;
     ">
     <h4>{title}</h4>
     '''
    for color, label in zip(colors, labels):
        legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:10px;"></i> {label}<br>'
    legend_html += '</div>'
    map_object.get_root().html.add_child(folium.Element(legend_html))
    return map_object

# Laad het JSON-bestand met stations (je moet het JSON-bestand in de juiste map plaatsen)
with open('.devcontainer/London stations.json', 'r') as f:
    stations_data = json.load(f)

# Neutrale basemap voor Londen
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10, tiles='OpenStreetMap')

# Voeg lagen toe voor elke zone (bijv. zone 1 tot 6)
zone_colors = {
    '1': 'red',
    '2': 'orange',
    '3': 'yellow',
    '4': 'yellowgreen',
    '5': 'green',
    '6': 'cyan'
}

# Maak lagen aan voor elke zone en voeg ze toe aan de kaart
for zone, color in zone_colors.items():
    m = create_zone_layer(stations_data, zone, m, color)

# Voeg de categorische legenda toe
m = add_categorical_legend(m, 'Station Types', 
                           colors=['red', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan'], 
                           labels=['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6'])

# Voeg de laagbesturing (layer control) toe zodat de gebruiker lagen kan aan/uitzetten
folium.LayerControl(position='bottomleft', collapsed=False).add_to(m)

# Streamlit code
st.title('London Underground Stations Map by Zone')

# Toon de kaart in Streamlit
st_data = st_folium(m, width=725, height=500)

import streamlit as st
import folium
import json
from streamlit_folium import st_folium


# Functie om een layer aan te maken voor een specifieke zone
def create_zone_layer(stations_data, zone, map_object, color):
    # Filter de stations voor de specifieke zone
    zone_layer = folium.FeatureGroup(name=f'Zone {zone}').add_to(map_object)
    
    for station in stations_data['features']:
        # Haal de zone van het station op
        station_zone = station['properties']['zone']
        
        # Voeg alleen stations toe die in de specifieke zone zitten
        if station_zone == zone:
            coords = station['geometry']['coordinates']
            name = station['properties']['name']
            marker_color = station['properties']['marker-color']
            
            # Voeg cirkelmarkeringen toe voor elk station in deze zone
            folium.Circle(
                location=[coords[1], coords[0]],  # Gebruik lat en lng
                popup=name,  # Laat de naam van het station zien
                tooltip=f"Station: {name}, Zone: {station_zone}",  # Toon station en zone in de tooltip
                color=marker_color,  # Gebruik de 'marker-color' als kleur voor de cirkel
                fill=True,
                fill_color=marker_color,  # Vulkleur gelijk aan de cirkelkleur
                fill_opacity=0.7,  # Vul de cirkel met transparantie
                radius=300  # Stel een vaste straal in
            ).add_to(zone_layer)
    
    return map_object

# Laad het JSON-bestand met stations (je moet het JSON-bestand in de juiste map plaatsen)
with open('.devcontainer/London stations.json', 'r') as f:
    stations_data = json.load(f)

# Neutrale basemap voor Londen
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10, tiles='OpenStreetMap')

# Voeg lagen toe voor elke zone (bijv. zone 1 tot 6)
zone_colors = {
    '1': 'red',
    '2': 'orange',
    '3': 'yellow',
    '4': 'yellowgreen',
    '5': 'green',
    '6': 'cyan'
}

# Maak lagen aan voor elke zone en voeg ze toe aan de kaart
for zone, color in zone_colors.items():
    m = create_zone_layer(stations_data, zone, m, color)

# Functie om een categorische legenda aan de kaart toe te voegen
def add_categorical_legend(map_object, title, colors, labels):
    legend_html = f'''
     <div style="position: fixed; 
     top: 10px; right: 10px; width: 150px; height: 180px; 
     background-color: white; z-index:9999; font-size:14px;
     padding: 10px;
     border: 2px solid grey;
     ">
     <h4>{title}</h4>
     '''
    for color, label in zip(colors, labels):
        legend_html += f'<i style="background:{color};width:18px;height:18px;float:left;margin-right:10px;"></i> {label}<br>'
    legend_html += '</div>'
    map_object.get_root().html.add_child(folium.Element(legend_html))
    return map_object

# Voeg de categorische legenda toe
m = add_categorical_legend(m, 'Station Types', 
                           colors=['red', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan'], 
                           labels=['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6'])

# Voeg de laagbesturing (layer control) toe zodat de gebruiker lagen kan aan/uitzetten
folium.LayerControl(position='bottomleft', collapsed=False).add_to(m)

# Streamlit code
st.title('London Underground Stations Map by Zone')

# Toon de kaart in Streamlit
st_data = st_folium(m, width=725, height=500)
