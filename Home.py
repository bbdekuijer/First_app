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

# Maak twee kolommen voor de data en de statistieken
col1, col2 = st.columns(2)

# Eerste kolom voor de eerste paar rijen van de dataset
with col1:
    st.subheader("👀 Eerste Kijk naar de Gegevens")
    st.dataframe(data.head(8))  # Laat de eerste 8 rijen van de dataset zien

# Tweede kolom voor de basisstatistieken
with col2:
    st.subheader("📊 Basis Statistieken")
    st.write(data.describe())  # Basisstatistieken van de dataset

