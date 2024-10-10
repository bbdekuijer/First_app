import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

# Bereken de groeisnelheid
# We nemen de logaritme van de totale waarden om een lineaire relatie te krijgen voor exponentiële groei
log_usage = np.log(usage_df['Totaal_Gebruik'])
years = usage_df['Jaar'] - usage_df['Jaar'].min()

# Gebruik een lineaire benadering voor de groeisnelheid
# Met np.polyfit passen we een rechte lijn aan de logaritmische waarden
slope, intercept = np.polyfit(years, log_usage, 1)

# Bereken de voorspelde waarden voor de jaren tot 2023
forecast_years = np.arange(2007, 2024) - 2007  # 2007 is ons startpunt
predicted_log_usage = intercept + slope * forecast_years
predicted_usage = np.exp(predicted_log_usage)  # Exponent van de voorspelde log-waarden om terug te gaan naar originele schaal

# Maak een Streamlit-titel
st.title('Metrogebruik van 2007 tot 2023 met Exponentiële Groei')

# Plot de werkelijke data en de voorspelde data
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(usage_df['Jaar'], usage_df['Totaal_Gebruik'], label='Werkelijke Data', color='blue')
ax.plot(np.arange(2007, 2024), predicted_usage, label='Exponentiële Groei (Voorspelling)', color='red', linestyle='--')
ax.set_title('Metrogebruik van 2007 tot 2023 (in Miljoenen)', fontsize=16)
ax.set_xlabel('Jaar', fontsize=12)
ax.set_ylabel('Totaal Metrogebruik (Miljoenen)', fontsize=12)
ax.legend()
ax.grid(True)

# Toon de plot in Streamlit
st.pyplot(fig)
