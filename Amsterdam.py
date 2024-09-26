import folium
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import streamlit as st
from streamlit_folium import st_folium

# Streamlit app title
st.title("Amsterdam Election Results by Stadsdeel")

# Data for total votes per party in each stadsdeel
stadsdeel_data = pd.DataFrame({
    'Stadsdeel': ['Centrum', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noord', 'Nieuw-West'],
    'VVD': [6925, 7054, 19318, 3347, 7315, 4576, 6910],
    'D66': [15804, 17686, 26210, 4297, 18430, 7465, 9757],
    'PVV (Partij voor de Vrijheid)': [1789, 2232, 5667, 1866, 2128, 4492, 4006],
    'CDA': [1144, 1128, 4112, 732, 1243, 1028, 1428],
    'SP (Socialistische Partij)': [2481, 2876, 5387, 2226, 2897, 2725, 2886],
    'Total Votes': [56596, 67786, 106662, 33351, 70863, 45085, 60317]  # Total votes per stadsdeel
})

# Calculate percentages for each party
partij_columns = ['VVD', 'D66', 'PVV (Partij voor de Vrijheid)', 'CDA', 'SP (Socialistische Partij)']
for partij in partij_columns:
    stadsdeel_data[partij + ' %'] = (stadsdeel_data[partij] / stadsdeel_data['Total Votes']) * 100

# Stadsdeel centroid coordinates
stadsdeel_coords = {
    'Centrum': [52.3728, 4.8936],
    'West': [52.3792, 4.8654],
    'Zuid': [52.3383, 4.8720],
    'Zuidoost': [52.3070, 4.9725],
    'Oost': [52.3625, 4.9415],
    'Noord': [52.4009, 4.9163],
    'Nieuw-West': [52.3600, 4.8103]
}

# Download the GeoJSON with stadsdeel boundaries
geojson_url = 'https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=INDELING_STADSDEEL&THEMA=gebiedsindeling'
response = requests.get(geojson_url)
geojson_data = response.json()

# Initialize the folium map centered on Amsterdam
amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=11)

# Add the GeoJSON layer with the stadsdelen boundaries
folium.GeoJson(geojson_data, name="Stadsdelen").add_to(amsterdam_map)

# Function to create pie charts and encode them as base64 using seaborn colors
def create_pie_chart(row):
    # Data for the pie chart
    labels = ['VVD', 'D66', 'PVV (Partij voor de Vrijheid)', 'CDA', 'SP (Socialistische Partij)']
    sizes = [row[partij + ' %'] for partij in labels]
    
    # Use seaborn color palette for better visuals
    colors = sns.color_palette("pastel")[0:5]
    
    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Save the pie chart as a PNG in memory
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close(fig)
    img.seek(0)
    
    # Encode the image in base64
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return img_base64

# Add markers and pop-ups with pie charts
for index, row in stadsdeel_data.iterrows():
    # Create the pie chart
    pie_chart_img = create_pie_chart(row)
    
    # HTML for the pop-up with the pie chart image
    html = f"""
    <b>{row['Stadsdeel']}</b><br>
    <img src="data:image/png;base64,{pie_chart_img}" style="width:200px;height:200px;">
    """
    
    iframe = folium.IFrame(html, width=220, height=220)
    popup = folium.Popup(iframe, max_width=250)
    
    # Get the coordinates for the current stadsdeel
    coords = stadsdeel_coords.get(row['Stadsdeel'], [52.3676, 4.9041])  # Fallback to default if not found
    
    # Add marker with the pie chart
    folium.Marker(
        location=coords,
        popup=popup
    ).add_to(amsterdam_map)

# Display the map using streamlit_folium
st_folium(amsterdam_map, width=725)
