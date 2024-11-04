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
        background-image: url("Afbeeldingen/Titanic.jpg");
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

# Navigatie
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Selecteer een pagina:", ["Data-analyse", "Visualisaties", "Machine Learning"])

# Sectiebeschrijvingen en inhoud
if page == "Data-analyse":
    st.write("In deze sectie kun je de dataset verkennen, basisstatistieken bekijken en ontbrekende waarden analyseren.")
    # Voeg hier de code voor data-analyse toe

elif page == "Visualisaties":
    st.write("Hier kun je verschillende grafieken en visualisaties van de data bekijken.")
    # Voeg hier de code voor visualisaties toe

elif page == "Machine Learning":
    st.write("In deze sectie kun je een machine learning model trainen en de prestaties evalueren.")
    # Voeg hier de code voor machine learning toe

# Belangrijkste Statistieken
st.subheader("Belangrijkste Statistieken")
st.write(f"Aantal passagiers: {data.shape[0]}")
st.write(f"Aantal overlevenden: {data[data['Survived'] == 1].shape[0]}")

