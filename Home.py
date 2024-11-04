import streamlit as st
import pandas as pd

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Introductie
st.write("Welkom bij de Titanic Data Analyse App. Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren met behulp van machine learning.")

# CSS voor styling
st.markdown(
    """
    <style>
    .image-container {
        position: fixed; 
        bottom: 10px; 
        left: 10px;
        z-index: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Afbeelding links onderin toevoegen
st.markdown(
    """
    <div class="image-container">
        <img src="Afbeeldingen/Titanic.jpg" alt="Titanic" style="width: 100px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Sectie voor data-analyse
st.header("Data-analyse")
st.subheader("Bekijk de gegevens")
st.dataframe(data.head())

# Statistieken
st.subheader("Basisstatistieken")
st.write(data.describe())
