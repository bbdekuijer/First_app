import streamlit as st
import pandas as pd

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Achtergrondafbeelding instellen
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("./Afbeeldingen/Titanic.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Introductie
st.write("Welkom bij de Titanic Data Analyse App. Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren met behulp van machine learning.")
