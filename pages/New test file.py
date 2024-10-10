import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Volledig pad naar de CSV-bestanden
filepath_b = ".devcontainer/334JourneyDataExtract07Sep2022-11Sep2022.csv"
filepath_w = ".devcontainer/df_temp_updated.csv"

# Laden van de Bikeshare data en weerdata
bike_data = pd.read_csv(filepath_b)
weather = pd.read_csv(filepath_w)

# Converteer de datums naar datetime-indeling met foutafhandeling
bike_data['Start Date'] = pd.to_datetime(bike_data['Start Date'], errors='coerce')
bike_data['End Date'] = pd.to_datetime(bike_data['End Date'], errors='coerce')
weather['Date'] = pd.to_datetime(weather['Date'], errors='coerce')

# Verwijder rijen met NaT waarden na conversie
bike_data = bike_data.dropna(subset=['Start Date', 'End Date'])
weather = weather.dropna(subset=['Date'])

# Titel van de Streamlit app
st.title('Fiets weer of niet?')

# Locatielijst opstellen
locations = bike_data['StartStation Name'].unique().tolist()

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
    filtered_bike_data = bike_data[bike_data['StartStation Name'] == selected_location]

# Groepeer de gefilterde data per dag en tel het aantal ritten
trips_per_day = filtered_bike_data.groupby(filtered_bike_data['Start Date'].dt.date).size().reset_index(name='Total Rides')

# Voeg weerdata toe aan de fietsritten per dag
trips_per_day['Start Date'] = pd.to_datetime(trips_per_day['Start Date'])
merged_data = pd.merge(trips_per_day, weather, left_on='Start Date', right_on='Date', how='left')

# Filter merged_data voor de laatste 7 dagen
last_7_days = merged_data['Start Date'].dt.date.unique()[-7:]  # Laatste 7 datums
merged_data = merged_data[merged_data['Start Date'].dt.date.isin(last_7_days)]

# Voeg een keuzemenu toe om te selecteren welke y-as weergeven wordt
yaxis_option = st.sidebar.selectbox(
    'Selecteer welke gegevens je wil weergeven:',
    options=['Gemiddelde Temperatuur', 'Regenval']
)

# Maak de plot met Plotly
fig = go.Figure()

# Voeg fietsritten toe
fig.add_trace(go.Scatter(x=merged_data['Start Date'], y=merged_data['Total Rides'], mode='lines+markers', name='Fietsritten', line=dict(color='blue')))

# Conditie voor het weergeven van de temperatuur of regenval
if yaxis_option == 'Gemiddelde Temperatuur':
    fig.add_trace(go.Scatter(x=merged_data['Start Date'], y=merged_data['tavg'], mode='lines', name='Gemiddelde Temperatuur', line=dict(color='red'), yaxis='y2'))
elif yaxis_option == 'Regenval':
    fig.add_trace(go.Bar(x=merged_data['Start Date'], y=merged_data['prcp'], name='Regenval (mm)', yaxis='y3', opacity=0.5))

# Update lay-out voor de plot
fig.update_layout(
    title='Zo ging het eraan toe: {}'.format(selected_location),
    xaxis_title='Datum',
    yaxis_title='Aantal Ritten',
    yaxis=dict(title='Aantal Ritten'),
    yaxis2=dict(title='Gemiddelde Temperatuur (°C)', overlaying='y', side='right', position=0.99),
    yaxis3=dict(title='Regenval (mm)', overlaying='y', side='right', position=0.99, showgrid=False),
    legend_title='Legenda',
    legend=dict(x=1.2, y=1, traceorder='normal', orientation='v'),
    xaxis=dict(
        tickmode='linear',
        dtick='1 day',
        tickformat='%Y-%m-%d',
        tickangle=-45
    )
)

# Toon de plot in Streamlit
st.plotly_chart(fig)


