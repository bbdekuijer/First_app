import streamlit as st
import pandas as pd

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Introductie
st.write("Welkom bij de Titanic Data Analyse App. Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren met behulp van machine learning.")

# Afbeelding links onderin toevoegen
st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; padding: 10px;">
        <img src="Afbeeldingen/Titanic.jpg" alt="Titanic" style="width: 100px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)
