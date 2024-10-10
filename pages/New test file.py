# Maak de plot met fietsritten en gemiddelde temperatuur
fig, ax1 = plt.subplots()

# Eerste plot voor fietsritten
ax1.plot(merged_data['Start date'], merged_data['Total Rides'], color='blue', label='Fietsritten')
ax1.set_xlabel('Datum')
ax1.set_ylabel('Aantal Ritten', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Tweede as voor temperatuur
ax2 = ax1.twinx()
ax2.plot(merged_data['Start date'], merged_data['tavg'], color='red', label='Gemiddelde Temperatuur')
ax2.set_ylabel('Gemiddelde Temperatuur (°C)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Formatteer de x-as om alleen de relevante datums weer te geven
ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Zorgt voor een integer-as
ax1.set_xticks(merged_data['Start date'])  # Zet de x-ticks op de datums van de datapunten
ax1.set_xticklabels(merged_data['Start date'].dt.strftime('%Y-%m-%d'), rotation=45)  # Formatteer de datums

# Titel en legenda
fig.suptitle('Fietsgebruik en Weersomstandigheden over Tijd')
fig.tight_layout()

# Toon de plot in Streamlit
st.pyplot(fig)



