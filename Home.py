import streamlit as st
import pandas as pd

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel met emoji
st.title("🛳️ Titanic Data Analyse App")

# Introductie met emoji
st.write("Welkom bij de Titanic Data Analyse App! 📊 Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren.")

# Informatie over de dataset
st.header("📁 Dataset Informatie")
st.write("Hieronder vind je een samenvatting van de Titanic dataset:")

# Toon de eerste paar rijen van de dataset
st.subheader("👀 Eerste Kijk naar de Gegevens")
st.dataframe(data.head())  # Laat de eerste 5 rijen van de dataset zien

# Statistieken van de dataset
st.subheader("📊 Basis Statistieken")
st.write(data.describe())  # Basisstatistieken van de dataset

# Sectie over de kolommen in de dataset
st.subheader("🗂️ Kolomnamen")
st.write("De Titanic dataset bevat de volgende kolommen:")
st.write(data.columns.tolist())  # Toon een lijst van kolomnamen

# Extra informatie
st.write("Gebruik de navigatie aan de zijkant om verder te gaan met data-analyse, visualisaties, of machine learning!")
