import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Pad naar de CSV bestanden in de .devcontainer map
df_temp_updated = pd.read_csv('.devcontainer/df_temp_updated.csv')
df_bike = pd.read_csv('.devcontainer/350JourneyDataExtract26Dec2022-01Jan2023.csv')

# Zorg ervoor dat de 'Start date' al is geconverteerd naar datetime
df_bike['Start date'] = pd.to_datetime(df_bike['Start date'])

# Extraheren van de datum uit de 'Start date' kolom
df_bike['Date'] = df_bike['Start date'].dt.date

# Groeperen op datum en het aantal ritten tellen
rides_per_date = df_bike.groupby('Date').size().reset_index(name='ride_count')

# Zorg ervoor dat de 'Date' kolom in df_temp_updated een datetime-object is
df_temp_updated['Date'] = pd.to_datetime(df_temp_updated['Date'])

# Selecteer de rijen waar de 'Date' tussen 2022-12-26 en 2023-01-01 ligt
start_date = '2022-12-26'
end_date = '2023-01-01'

# Filter de data voor de opgegeven datums
df_temp_filtered = df_temp_updated[(df_temp_updated['Date'] >= start_date) & (df_temp_updated['Date'] <= end_date)]

# Zorg ervoor dat de 'Date' kolommen van beide DataFrames hetzelfde type hebben (datum object)
df_temp_filtered.loc[:, 'Date'] = pd.to_datetime(df_temp_filtered['Date'])
rides_per_date['Date'] = pd.to_datetime(rides_per_date['Date'])

# Merge de DataFrames op basis van de 'Date' kolom
df_combined = pd.merge(df_temp_filtered, rides_per_date, on='Date', how='left')

# Zet de beschikbare variabelen in een lijst
variables = ['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres']

# Voeg een selectbox toe voor variabele selectie
selected_variable = st.selectbox('Selecteer een variabele voor de rechter Y-as', variables)

# Zorg ervoor dat de 'Date' kolom een datetime-object is
df_combined['Date'] = pd.to_datetime(df_combined['Date'])

# Maak de interactieve grafiek met Plotly
fig = go.Figure()

# Voeg de 'ride_count' data toe aan de linker Y-as
fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined['ride_count'], mode='lines', name='Aantal ritten', yaxis='y1'))

# Voeg de geselecteerde variabele toe aan de rechter Y-as
fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined[selected_variable], mode='lines', name=selected_variable.capitalize(), yaxis='y2'))

# Update layout voor dubbele Y-assen
fig.update_layout(
    title="Interactief Fietsgebruik en Weersdata",
    xaxis_title="Datum",
    yaxis=dict(
        title="Aantal ritten",
        titlefont=dict(color="blue"),
        tickfont=dict(color="blue"),
        side="left"
    ),
    yaxis2=dict(
        title="",
        titlefont=dict(color="green"),
        tickfont=dict(color="green"),
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode="x"
)

# Voeg eenheden toe aan de rechter Y-as op basis van de geselecteerde variabele
if selected_variable == 'tavg':
    fig.layout.yaxis2.title = "Gemiddelde Temperatuur (°C)"
elif selected_variable == 'tmin':
    fig.layout.yaxis2.title = "Minimale Temperatuur (°C)"
elif selected_variable == 'tmax':
    fig.layout.yaxis2.title = "Maximale Temperatuur (°C)"
elif selected_variable == 'prcp':
    fig.layout.yaxis2.title = "Neerslag (mm)"
elif selected_variable == 'wspd':
    fig.layout.yaxis2.title = "Windsnelheid (km/u)"
elif selected_variable == 'pres':
    fig.layout.yaxis2.title = "Luchtdruk (hPa)"

# Render de grafiek in Streamlit
st.plotly_chart(fig)
