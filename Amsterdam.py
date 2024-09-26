import folium
import pandas as pd
import requests
import streamlit as st  # Voor Streamlit functionaliteit
from streamlit_folium import st_folium  # Voor het renderen van de folium kaart

# Titel van de applicatie
st.title("Verkiezingsuitslagen 2021 Amsterdam")

# Beschrijving
st.write("""
Deze kaart toont de verdeling van stemmen op de vijf grootste politieke partijen per stadsdeel in Amsterdam.
De kleur van elk stadsdeel is gebaseerd op de grootste partij in dat stadsdeel.
""")

# Data voor het aantal stemmen per partij in elk stadsdeel
stadsdeel_data = pd.DataFrame({
    'Stadsdeel': ['Centrum', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noord', 'Nieuw-West'],
    'VVD': [6925, 7054, 19318, 3347, 7315, 4576, 6910],
    'D66': [15804, 17686, 26210, 4297, 18430, 7465, 9757],
    'PVV': [1789, 2232, 5667, 1866, 2128, 4492, 4006],
    'CDA': [1144, 1128, 4112, 732, 1243, 1028, 1428],
    'SP': [2481, 2876, 5387, 2226, 2897, 2725, 2886],
    'Total Votes': [56596, 67786, 106662, 33351, 70863, 45085, 60317]
})

# Bereken de percentages per partij
for partij in ['VVD', 'D66', 'PVV', 'CDA', 'SP']:
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

# Functie om de grootste partij per stadsdeel te bepalen
def get_largest_party(row):
    partijen = ['VVD', 'D66', 'PVV', 'CDA', 'SP']
    return max(partijen, key=lambda partij: row[partij])

# Voeg een kolom toe met de grootste partij per stadsdeel
stadsdeel_data['Grootste Partij'] = stadsdeel_data.apply(get_largest_party, axis=1)

# Kleurenschema voor de grootste partijen
party_colors = {
    'VVD': '#1f77b4',
    'D66': '#2ca02c',
    'PVV': '#ff7f0e',
    'CDA': '#d62728',
    'SP': '#9467bd'
}

# Download de GeoJSON met stadsdeelgrenzen van Amsterdam
geojson_url = 'https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=INDELING_STADSDEEL&THEMA=gebiedsindeling'
response = requests.get(geojson_url)
geojson_data = response.json()

# Maak de folium kaart
amsterdam_map = folium.Map(location=[52.3676, 4.9041], zoom_start=11)

# Voeg de GeoJSON laag toe en kleur per grootste partij
folium.GeoJson(
    geojson_data,
    name="Stadsdelen",
    style_function=lambda feature: {
        'fillColor': party_colors[stadsdeel_data[stadsdeel_data['Stadsdeel'] == feature['properties']['Stadsdeel']]['Grootste Partij'].values[0]],
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }
).add_to(amsterdam_map)

# Voeg markers en pop-ups toe met de percentages per partij per stadsdeel
for index, row in stadsdeel_data.iterrows():
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
    
    coords = stadsdeel_coords.get(row['Stadsdeel'], [52.3676, 4.9041])  # Fallback indien niet gevonden
    
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_text, max_width=300)  # Vergroot de breedte van de pop-up
    ).add_to(amsterdam_map)

# Voeg een legenda toe voor de grootste partijen
legend_html = '''
 <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 150px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
 <h4 style="margin-left: 10px;">Grootste Partij per Stadsdeel</h4>
 <i style="background: #1f77b4"></i> VVD<br>
 <i style="background: #2ca02c"></i> D66<br>
 <i style="background: #ff7f0e"></i> PVV<br>
 <i style="background: #d62728"></i> CDA<br>
 <i style="background: #9467bd"></i> SP<br>
 </div>
 '''
amsterdam_map.get_root().html.add_child(folium.Element(legend_html))

# Toon de kaart in Streamlit
st_folium(amsterdam_map, width=725)

import os
import pandas as pd
import streamlit as st

# Check current working directory
print(os.getcwd())

# Set working directory (change to a relative path if needed)
path = './'  # Relative path to your CSV file
os.chdir(path)

# Load the CSV file (make sure the file is in the same directory as this script)
stemmen_ams = pd.read_csv('2021 stemmen Amsterdam.csv')

# Clean the data by dropping rows with all NaN values and resetting the index
stemmen_cleaned = stemmen_ams.dropna(how='all').reset_index(drop=True)

# Rename the first valid row as the header and drop the previous header rows
stemmen_cleaned.columns = stemmen_cleaned.iloc[1]
stemmen_cleaned = stemmen_cleaned.drop([0, 1]).reset_index(drop=True)

# Streamlit app: Creating columns
col1, col2 = st.columns([3, 1])  # col1 is wider, col2 is smaller (for the legend)

# In col2 (right column), we place the legend
with col2:
    st.subheader('Legenda')
    st.write("""
    - **Dropdown Menu:** kies een regio uit de lijst.
    - **Slider:** Verschuif de slider om het aantal partijen te kiezen tussen 0 en 33.
    - **Checkbox:** Vink deze aan om extra informatie te tonen.
    """)

# In col1 (left column), we place the interactive widgets
with col1:
    # Dropdown menu
    opties = ["amsterdam", "centrum", "oost", "zuid", "west", "noord", "nieuw_west", "zuidoost"]
    geselecteerde_optie = st.selectbox('Kies een regio:', opties)
    st.write(f"Geselecteerde regio: {geselecteerde_optie}")

    # Navigation logic based on the selected region
    if geselecteerde_optie == "amsterdam":
        st.subheader("Welkom in Amsterdam!")
        st.write("""
        Amsterdam is de hoofdstad van Nederland en bekend om zijn grachten, musea, 
        en rijke geschiedenis. Het is een diverse stad met verschillende wijken die
        elk hun eigen karakter hebben.
        """)

    elif geselecteerde_optie == "centrum":
        st.subheader("Welkom in het Centrum van Amsterdam!")
        st.write("""
        Het centrum van Amsterdam is het oudste en meest toeristische deel van de stad. 
        Het is bekend om de prachtige grachten, historische gebouwen, het Koninklijk Paleis,
        de Dam en het Anne Frank Huis.
        """)

    elif geselecteerde_optie == "oost":
        st.subheader("Welkom in Amsterdam Oost!")
        st.write("""
        Amsterdam Oost is een diverse wijk met zowel traditionele als moderne architectuur. 
        Het Oosterpark en Artis zijn bekende trekpleisters, evenals de culturele smeltkroes 
        van de Dappermarkt.
        """)

    elif geselecteerde_optie == "zuid":
        st.subheader("Welkom in Amsterdam Zuid!")
        st.write("""
        Amsterdam Zuid staat bekend om het Museumplein, waar je het Rijksmuseum, 
        Van Gogh Museum en het Stedelijk Museum kunt vinden. Het is een van de luxere wijken 
        van de stad, met veel winkels en restaurants.
        """)

    elif geselecteerde_optie == "west":
        st.subheader("Welkom in Amsterdam West!")
        st.write("""
        Amsterdam West is een diverse buurt met een mix van culturen. Het Westerpark 
        is een populaire ontmoetingsplek, en de wijk staat bekend om zijn gezellige markten 
        en restaurants.
        """)

    elif geselecteerde_optie == "noord":
        st.subheader("Welkom in Amsterdam Noord!")
        st.write("""
        Amsterdam Noord is een snelgroeiend deel van de stad. Vroeger een industriële zone, 
        maar tegenwoordig bekend om moderne wijken en culturele hotspots zoals de NDSM-werf.
        """)

    elif geselecteerde_optie == "nieuw_west":
        st.subheader("Welkom in Amsterdam Nieuw-West!")
        st.write("""
        Amsterdam Nieuw-West is een van de grootste stadsdelen van de stad. Het biedt veel 
        ruimte en groen, en er zijn veel nieuwbouwwoningen. Het Sloterpark en Sloterplas zijn 
        favoriete recreatiegebieden.
        """)

    elif geselecteerde_optie == "zuidoost":
        st.subheader("Welkom in Amsterdam Zuidoost!")
        st.write("""
        Amsterdam Zuidoost is een multiculturele wijk en bekend vanwege de Johan Cruijff Arena, 
        het winkelcentrum de Amsterdamse Poort, en diverse concertzalen zoals de Ziggo Dome en AFAS Live.
        """)

# Predefined list of parties and votes
parties = [
    'D66', 'VVD', 'GROENLINKS', 'Partij van de Arbeid (P.v.d.A.)', 'Partij voor de Dieren',
    'DENK', 'Volt', 'BIJ1', 'PVV (Partij voor de Vrijheid)', 'SP (Socialistische Partij)',
    'Forum voor Democratie', 'CDA', 'ChristenUnie', 'JA21', 'NIDA', '50PLUS', 'JONG',
    'CODE ORANJE', 'Staatkundig Gereformeerde Partij (SGP)', 'Piratenpartij', 
    'Trots op Nederland (TROTS)', 'LP (Libertaire Partij)', 'Splinter', 'JEZUS LEEFT', 
    'NLBeter', 'BBB', 'OPRECHT', 'U-Buntu Connected Front', 'Partij voor de Republiek', 
    'De Groenen', 'Partij van de Eenheid', 'Lijst Henk Krol', 'Vrij en Sociaal Nederland'
]

votes = [
    99649, 55445, 44907, 32783, 30880, 29384, 25988, 25563, 22180, 21478, 11971, 
    10815, 6214, 5282, 5053, 2355, 1278, 864, 586, 391, 384, 383, 343, 301, 297, 
    276, 247, 221, 151, 151, 144, 106, 89
]

# Create DataFrame for parties and votes
parties_df = pd.DataFrame({'Party': parties, 'Votes': votes})

# Slider to select the number of parties
num_parties = st.slider('Selecteer het aantal partijen om mee te rekenen:', min_value=1, max_value=len(parties), value=10)

# Sort by votes and display top parties based on the selection
top_parties = parties_df.sort_values(by='Votes', ascending=False).head(num_parties)

# Display results
st.write(f"De top {num_parties} partijen op basis van stemmen zijn:")
st.write(top_parties)
