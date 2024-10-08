import folium
import pandas as pd 

import folium
import json

# Laad het JSON-bestand met stations
with open('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/London stations.json', 'r') as f:
    stations_data = json.load(f)

# Maak de kaart met een normale OpenStreetMap achtergrond
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10, tiles='OpenStreetMap')

# Loop door de stationsdata en voeg cirkelvormige markeringen toe
for station in stations_data['features']:
    # Stel de eigenschappen van het station in
    coords = station['geometry']['coordinates']
    name = station['properties']['name']
    marker_color = station['properties']['marker-color']
    
    # Voeg cirkelmarkeringen toe voor elk station
    folium.Circle(
        location=[coords[1], coords[0]],  # Gebruik lat en lng
        popup=name,  # Laat de naam van het station zien
        tooltip=f"Station: {name}, Zone: {station['properties']['zone']}",  # Toon station en zone in de tooltip
        color=marker_color,  # Gebruik de 'marker-color' als kleur voor de cirkel
        fill=True,
        fill_color=marker_color,  # Vulkleur gelijk aan de cirkelkleur
        fill_opacity=0.7,  # Vul de cirkel met transparantie
        radius=300  # Stel een vaste straal in
    ).add_to(m)

# Functie om een categorische legenda aan de kaart toe te voegen
def add_categorical_legend(map_object, title, colors, labels):
    legend_html = f'''
     <div style="position: fixed; 
     top: 10px; right: 10px; width: 150px; height: 200px; 
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
                           colors=['red', 'orange', 'yellow', 'yellowgreen', 'green', 'cyan', 'white'], 
                        labels=['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'zone 7/8'])
# Toon de kaart
m


import pandas as pd
import matplotlib.pyplot as plt

# Load your metro dataset
metro_data = pd.read_csv('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/2017_Entry_Exit.csv')

# Summarize total usage for each station
metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
plt.figure(figsize=(12, 8))
plt.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
plt.xlabel('Total Metro Usage')
plt.ylabel('Stations')
plt.title('Top 25 Busiest Stations in London')
plt.gca().invert_yaxis()  # Invert the y-axis to display the busiest station on top
plt.tight_layout()
plt.show()

# Find peak times for each station by comparing weekday vs. weekend
metro_data['peak_time'] = metro_data[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Get peak times for the top 25 stations
top_25_stations_with_peak = metro_data[metro_data['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]

# Display the top 25 stations with peak times
print(top_25_stations_with_peak)


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load your metro dataset
metro_data = pd.read_csv('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/2017_Entry_Exit.csv')

# Assuming your metro dataset has 'Month' column with values from 1 (January) to 12 (December)
# If you don't have a 'Month' column, you can extract the month from a 'Date' column
# Uncomment below if needed
# metro_data['Date'] = pd.to_datetime(metro_data['Date'])
# metro_data['Month'] = metro_data['Date'].dt.month

# Create an interactive slider to select the month
selected_month = st.slider('Select a month', 1, 12, 1)

# Filter the data based on the selected month
metro_data_filtered = metro_data[metro_data['Month'] == selected_month]

# Summarize total usage for each station in the selected month
metro_data_filtered['total_usage'] = metro_data_filtered['Entry_Week'] + metro_data_filtered['Entry_Saturday'] + metro_data_filtered['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data_filtered[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
ax.set_xlabel('Total Metro Usage')
ax.set_ylabel('Stations')
ax.set_title(f'Top 25 Busiest Stations in London - Month: {selected_month}')
ax.invert_yaxis()  # Invert the y-axis to display the busiest station on top
st.pyplot(fig)

# Find peak times for each station by comparing weekday vs. weekend
metro_data_filtered['peak_time'] = metro_data_filtered[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Display peak times for the top 25 stations
top_25_stations_with_peak = metro_data_filtered[metro_data_filtered['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]
st.dataframe(top_25_stations_with_peak)









