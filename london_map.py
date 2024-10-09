import streamlit as st
import folium
import json
from streamlit_folium import st_folium

st.cache_data
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
import pandas as pd
import matplotlib.pyplot as plt

# Load your metro dataset
metro_data = pd.read_csv('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/2017_Entry_Exit.csv')

# Summarize total usage for each station
metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
st.title('Top 25 Busiest Stations in London')
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
ax.set_xlabel('Total Metro Usage')
ax.set_ylabel('Stations')
ax.set_title('Top 25 Busiest Stations in London')
ax.invert_yaxis()  # Invert the y-axis to display the busiest station on top
st.pyplot(fig)

# Find peak times for each station by comparing weekday vs. weekend
metro_data['peak_time'] = metro_data[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Get peak times for the top 25 stations
top_25_stations_with_peak = metro_data[metro_data['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]

# Display the top 25 stations with peak times
st.subheader('Top 25 Stations with Peak Times')
st.write(top_25_stations_with_peak)


# Load the weather dataset
weather_data= pd.read_csv('/Users/casijnvantill/Downloads/weather_london.csv')

# Rename the date column
weather_data.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

# Convert the date column to datetime format
weather_data['date'] = pd.to_datetime(weather_data['date'])

# Extract the month and year from the date
weather_data['month'] = weather_data['date'].dt.month
weather_data['year'] = weather_data['date'].dt.year

# Group by month to get the total precipitation per month
monthly_precipitation = weather_data.groupby('month')['prcp'].sum()

# Plot the histogram of monthly precipitation
st.title('Monthly Precipitation in London')
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(monthly_precipitation.index, monthly_precipitation.values)
ax2.set_title('Monthly Precipitation in London')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Precipitation (mm)')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig2)

# Grouping the data by month to get average temperatures (tavg, tmin, tmax) per month
monthly_temperatures = weather_data.groupby('month')[['tavg', 'tmin', 'tmax']].mean()

# Plotting the monthly average, minimum, and maximum temperatures
st.title('Monthly Temperatures in London')
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.plot(monthly_temperatures.index, monthly_temperatures['tavg'], label='Avg Temp', marker='o')
ax3.plot(monthly_temperatures.index, monthly_temperatures['tmin'], label='Min Temp', marker='o')
ax3.plot(monthly_temperatures.index, monthly_temperatures['tmax'], label='Max Temp', marker='o')
ax3.set_title('Monthly Temperatures in London')
ax3.set_xlabel('Month')
ax3.set_ylabel('Temperature (°C)')
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax3.legend()
st.pyplot(fig3)
