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
    opties = ["Amsterdam", "Centrum", "Oost", "Zuid", "West", "Noord", "Nieuw_West", "Zuidoost"]
    geselecteerde_optie = st.selectbox('Kies een regio:', opties)
    st.write(f"Geselecteerde regio: {geselecteerde_optie}")

    # Navigation logic based on the selected region
    if geselecteerde_optie == "Amsterdam":
        st.subheader("Welkom in Amsterdam!")
        st.write("""
        Amsterdam is de hoofdstad van Nederland en bekend om zijn grachten, musea, 
        en rijke geschiedenis. Het is een diverse stad met verschillende wijken die
        elk hun eigen karakter hebben.
        """)

    elif geselecteerde_optie == "Centrum":
        st.subheader("Welkom in het Centrum van Amsterdam!")
        st.write("""
        Het centrum van Amsterdam is het oudste en meest toeristische deel van de stad. 
        Het is bekend om de prachtige grachten, historische gebouwen, het Koninklijk Paleis,
        de Dam en het Anne Frank Huis.
        """)

    elif geselecteerde_optie == "Oost":
        st.subheader("Welkom in Amsterdam Oost!")
        st.write("""
        Amsterdam Oost is een diverse wijk met zowel traditionele als moderne architectuur. 
        Het Oosterpark en Artis zijn bekende trekpleisters, evenals de culturele smeltkroes 
        van de Dappermarkt.
        """)

    elif geselecteerde_optie == "Zuid":
        st.subheader("Welkom in Amsterdam Zuid!")
        st.write("""
        Amsterdam Zuid staat bekend om het Museumplein, waar je het Rijksmuseum, 
        Van Gogh Museum en het Stedelijk Museum kunt vinden. Het is een van de luxere wijken 
        van de stad, met veel winkels en restaurants.
        """)

    elif geselecteerde_optie == "West":
        st.subheader("Welkom in Amsterdam West!")
        st.write("""
        Amsterdam West is een diverse buurt met een mix van culturen. Het Westerpark 
        is een populaire ontmoetingsplek, en de wijk staat bekend om zijn gezellige markten 
        en restaurants.
        """)

    elif geselecteerde_optie == "Noord":
        st.subheader("Welkom in Amsterdam Noord!")
        st.write("""
        Amsterdam Noord is een snelgroeiend deel van de stad. Vroeger een industriële zone, 
        maar tegenwoordig bekend om moderne wijken en culturele hotspots zoals de NDSM-werf.
        """)

    elif geselecteerde_optie == "Nieuw_West":
        st.subheader("Welkom in Amsterdam Nieuw-West!")
        st.write("""
        Amsterdam Nieuw-West is een van de grootste stadsdelen van de stad. Het biedt veel 
        ruimte en groen, en er zijn veel nieuwbouwwoningen. Het Sloterpark en Sloterplas zijn 
        favoriete recreatiegebieden.
        """)

    elif geselecteerde_optie == "Zuidoost":
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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Laad het CSV-bestand
stemmen_ams = pd.read_csv('2021 stemmen Amsterdam.csv')

# Verwijder rijen met alleen NaN-waarden en reset de index
stemmen_cleaned = stemmen_ams.dropna(how='all').reset_index(drop=True)

# Hernoem de eerste geldige rij als header en verwijder de vorige header-rijen
stemmen_cleaned.columns = stemmen_cleaned.iloc[1]
stemmen_cleaned = stemmen_cleaned.drop([0, 1]).reset_index(drop=True)

# Verwijder de eerste kolom (indien nodig)
stemmen_cleaned = stemmen_cleaned.drop(stemmen_cleaned.columns[0], axis=1)

# Zet de kolommen om naar numerieke waarden, forceer fouten naar NaN
stemmen_cleaned['opgeroepenen'] = pd.to_numeric(stemmen_cleaned['opgeroepenen'], errors='coerce')
stemmen_cleaned['geldige stembiljetten'] = pd.to_numeric(stemmen_cleaned['geldige stembiljetten'], errors='coerce')
stemmen_cleaned['blanco stembiljetten'] = pd.to_numeric(stemmen_cleaned['blanco stembiljetten'], errors='coerce')
stemmen_cleaned['ongeldige stembiljetten'] = pd.to_numeric(stemmen_cleaned['ongeldige stembiljetten'], errors='coerce')
stemmen_cleaned['aangetroffen stembiljetten'] = pd.to_numeric(stemmen_cleaned['aangetroffen stembiljetten'], errors='coerce')

# Eerst, groepeer per stadsdeel en bereken de som van 'opgeroepenen' en 'aangetroffen stembiljetten'
groepering = stemmen_cleaned.groupby('stadsdeel')[['opgeroepenen', 'aangetroffen stembiljetten']].sum()

# Bereken het percentage van gestemde mensen per stadsdeel
groepering['percentage_gestemd'] = (groepering['aangetroffen stembiljetten'] / groepering['opgeroepenen']) * 100

# Stel de stadsdeelnamen en het percentage gestemd in
stadsdelen = groepering.index
percentages = groepering['percentage_gestemd']

# Voeg een titel toe aan de Streamlit-app
st.title("Stempercentage per Stadsdeel in Amsterdam (2021)")

# Beschrijvende tekst
st.write("Deze grafiek toont het percentage van gestemde mensen per stadsdeel in Amsterdam tijdens de Tweede Kamerverkiezingen van 2021. Optioneel kun je de nationale opkomstlijn weergeven door de checkbox hieronder aan te vinken.")

# Checkbox voor het tonen van de nationale opkomstlijn
toon_nationale_opkomst = st.checkbox('Toon nationale opkomstlijn')

# Maak een figure en plot het histogram
plt.figure(figsize=(10, 6))  # Zorg voor een grotere figuur om ruimte te maken voor de stadsdeelnamen
plt.bar(stadsdelen, percentages)

# Voeg de referentielijn toe voor de nationale opkomst als de checkbox is aangevinkt
if toon_nationale_opkomst:
    nationale_opkomst = 78.71
    plt.axhline(y=nationale_opkomst, color='r', linestyle='--', label='Nationale Opkomst (78.71%)')

# Labels en titel
plt.xlabel('Stadsdeel', fontsize=12)
plt.ylabel('Percentage Gestemd (%)', fontsize=12)
plt.title('Percentage Gestemd per Stadsdeel', fontsize=14)

# Draai de stadsdeelnamen verticaal zodat ze leesbaar zijn
plt.xticks(rotation=90, fontsize=10)

# Alleen een legenda tonen als de nationale opkomstlijn is ingeschakeld
if toon_nationale_opkomst:
    plt.legend()

# Toon de grafiek in Streamlit
st.pyplot(plt)

# Zorg ervoor dat je de figuur opnieuw instelt, zodat deze niet in de volgende weergave wordt hergebruikt
plt.clf()
