import streamlit as st
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
pip install scipy


# Definieer het exponentiële groeimodel
def exponential_growth(x, a, b):
    return a * np.exp(b * x)

# Laad de metro datasets voor de verschillende jaren
data_files = {
    2017: '.devcontainer/2017_Entry_Exit.csv',
    2016: '.devcontainer/2016_Entry_Exit.csv',
    2015: '.devcontainer/2015_Entry_Exit.csv',
    2014: '.devcontainer/2014_Entry_Exit.csv',
    2013: '.devcontainer/2013_Entry_Exit.csv',
    2012: '.devcontainer/2012_Entry_Exit.csv',
    2011: '.devcontainer/2011_Entry_Exit.csv',
    2010: '.devcontainer/2010_Entry_Exit.csv',
    2009: '.devcontainer/2009_Entry_Exit.csv',
    2008: '.devcontainer/2008_Entry_Exit.csv',
    2007: '.devcontainer/2007_Entry_Exit.csv'
}

# Maak een lege dictionary om het totale gebruik per jaar op te slaan
yearly_usage = {}

# Loop door elk bestand, bereken het totale gebruik en sla het op in de dictionary
for year, file in data_files.items():
    metro_data = pd.read_csv(file)
    metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']
    yearly_usage[year] = metro_data['total_usage'].sum()

# Zet de dictionary met jaarlijks gebruik om naar een DataFrame
usage_df = pd.DataFrame(list(yearly_usage.items()), columns=['Jaar', 'Totaal_Gebruik'])

# Verklein het gebruik naar miljoenen
usage_df['Totaal_Gebruik'] = usage_df['Totaal_Gebruik'] / 1e6

# Definieer de jaren en het gebruik voor het passen van het model
x_data = usage_df['Jaar'] - usage_df['Jaar'].min()  # Begin de jaren vanaf 0 voor betere fitting
y_data = usage_df['Totaal_Gebruik']

# Pas het exponentiële groeimodel toe op de data
popt, pcov = curve_fit(exponential_growth, x_data, y_data)

# Maak een array van jaren van 2007 tot 2023
years = np.arange(2007, 2024)
x_forecast = years - usage_df['Jaar'].min()  # Verschuif de voorspelde jaren

# Voorspel het metrogebruik met behulp van het model
predicted_usage = exponential_growth(x_forecast, *popt)

# Maak een Streamlit-titel
st.title('Metrogebruik van 2007 tot 2023 met Exponentiële Groei')

# Plot de werkelijke data en de voorspelde data
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(usage_df['Jaar'], usage_df['Totaal_Gebruik'], label='Werkelijke Data', color='blue')
ax.plot(years, predicted_usage, label='Exponentiële Groei (Voorspelling)', color='red', linestyle='--')
ax.set_title('Metrogebruik van 2007 tot 2023 (in Miljoenen)', fontsize=16)
ax.set_xlabel('Jaar', fontsize=12)
ax.set_ylabel('Totaal Metrogebruik (Miljoenen)', fontsize=12)
ax.legend()
ax.grid(True)

# Toon de plot in Streamlit
st.pyplot(fig)
