import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import urllib.request

# URL naar het CSV-bestand
url = "https://cycling.data.tfl.gov.uk/usage-stats/338JourneyDataExtract03Oct2022-09Oct2022.csv"

# Functie om de data in te lezen
@st.cache
def load_data(url):
    # Maak een request met een aangepaste user-agent
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    # Open de URL en lees de data in
    with urllib.request.urlopen(req) as response:
        data = pd.read_csv(response)
    
    return data

# Data laden
bike_data = load_data(url)

# Bestandslocatie voor weerdata
filepath_w = "/Users/jelskedeboer/Library/CloudStorage/OneDrive-HvA/Minor Data Science/London Case/Minor Data Science - 1072024 - 227 PM/weather_london.csv"
weather = pd.read_csv(filepath_w)

# Weerdata voorbereiden
weather = weather.rename(columns={'Unnamed: 0': 'date'})
weather = weather[['date', 'tavg', 'prcp', 'snow']].copy()
weather['date'] = pd.to_datetime(weather['date'])
weather = weather.fillna(0)

# Converteer de datums naar datetime-indeling
bike_data['Start date'] = pd.to_datetime(bike_data['Start date'])
bike_data['End date'] = pd.to_datetime(bike_data['End date'])

# Titel van de Streamlit app
st.title('Fiets weer of niet?')

# Locatielijst opstellen
locations = bike_data['Start station'].unique().tolist()

# Checkbox voor totaal
show_total = st.sidebar.checkbox('Toon data voor alle locaties')

# Dropdown voor locatie-selectie, afhankelijk van de checkbox
if show_total:
    selected_location = 'Totaal'
else:
    selected_location = st.sidebar.selectbox('Selecteer een locatie', locations)

# Filter de data op basis van de geselecteerde locatie
if selected_location == 'Totaal':
    filtered_bike_data = bike_data
else:
    filtered_bike_data = bike_data[bike_data['Start station'] == selected_location]

# Vraag de gebruiker om een datumbereik te selecteren
start_date, end_date = st.sidebar.date_input("Selecteer datumbereik:", [filtered_bike_data['Start date'].min(), filtered_bike_data['Start date'].max()])

# Filter de fietsdata en weerdata op basis van de geselecteerde datums
filtered_bike_data = filtered_bike_data[(filtered_bike_data['Start date'] >= pd.to_datetime(start_date)) & (filtered_bike_data['Start date'] <= pd.to_datetime(end_date))]
filtered_weather = weather[(weather['date'] >= pd.to_datetime(start_date)) & (weather['date'] <= pd.to_datetime(end_date))]

# Groepeer de gefilterde data per dag en tel het aantal ritten
trips_per_day = filtered_bike_data.groupby(filtered_bike_data['Start date'].dt.date).size().reset_index(name='Total Rides')

# Voeg weerdata toe aan de fietsritten per dag
trips_per_day['Start date'] = pd.to_datetime(trips_per_day['Start date'])
merged_data = pd.merge(trips_per_day, filtered_weather, left_on='Start date', right_on='date', how='left')

# Voeg een keuzemenu toe om te selecteren welke y-as weergeven wordt
yaxis_option = st.sidebar.selectbox(
    'Selecteer welke gegevens je wil weergeven:',
    options=['Gemiddelde Temperatuur', 'Regenval']
)

# Maak de plot met Plotly
fig = go.Figure()

# Voeg fietsritten toe
fig.add_trace(go.Scatter(x=merged_data['Start date'], y=merged_data['Total Rides'], mode='lines+markers', name='Fietsritten', line=dict(color='blue')))

# Conditie voor het weergeven van de temperatuur of regenval
if yaxis_option == 'Gemiddelde Temperatuur':
    fig.add_trace(go.Scatter(x=merged_data['Start date'], y=merged_data['tavg'], mode='lines', name='Gemiddelde Temperatuur', line=dict(color='red'), yaxis='y2'))
elif yaxis_option == 'Regenval':
    fig.add_trace(go.Bar(x=merged_data['Start date'], y=merged_data['prcp'], name='Regenval (mm)', yaxis='y3', opacity=0.5))

# Update lay-out voor de plot
fig.update_layout(
    title='Zo ging het eraan toe: {}'.format(selected_location),
    xaxis_title='Datum',
    yaxis_title='Aantal Ritten',
    yaxis=dict(title='Aantal Ritten'),
    yaxis2=dict(title='Gemiddelde Temperatuur (°C)', overlaying='y', side='right', position=0.99),  # Y-as voor temperatuur verder naar rechts
    yaxis3=dict(title='Regenval (mm)', overlaying='y', side='right', position=0.99, showgrid=False),  # Y-as voor regenval verder naar rechts buiten het plotgebied
    legend_title='Legenda',
    legend=dict(x=1.2, y=1, traceorder='normal', orientation='v'),  # Legenda buiten de grafiek
    xaxis=dict(
        tickmode='linear',
        dtick='1 day',
        tickformat='%Y-%m-%d',
        tickangle=-45
    )
)

# Toon de plot in Streamlit
st.plotly_chart(fig)

