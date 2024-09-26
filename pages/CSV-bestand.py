import streamlit as st
import pandas as pd

# Laad de CSV-bestand
csv_file = '2021 stemmen Amsterdam.csv'  # Zorg ervoor dat dit bestand in dezelfde map staat
data = pd.read_csv(csv_file)

# Hoofd Streamlit-app
st.title("Stemverdeling per Stadsdeel in Amsterdam")

# Geef een korte uitleg
st.write("Hier is de stemdata per stadsdeel in Amsterdam. Je kunt de data downloaden via de onderstaande link.")

# Geef de CSV-data weer als tabel
st.dataframe(data)

# Maak de CSV beschikbaar voor download
@st.cache_data
def convert_df(df):
    # Converteer DataFrame naar CSV
    return df.to_csv(index=False).encode('utf-8')

# Voeg een download knop toe
csv = convert_df(data)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='2021_stemmen_amsterdam.csv',
    mime='text/csv',
)
