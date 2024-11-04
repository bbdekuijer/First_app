import streamlit as st

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Introductie
st.write("Welkom bij de Titanic Data Analyse App! Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren.")

# Secties zonder navigatie
st.header("Secties:")
st.write("[Data Analyse](pages/01_Data_analyse.py)")
st.write("[Visualisatie](pages/02_Visualisatie.py)")
st.write("[Algoritme](pages/03_Algoritme.py)")

# Korte uitleg over de secties
st.write("Kies een van de bovenstaande secties om verder te gaan met de analyse, visualisatie of machine learning van de Titanic dataset.")
