import streamlit as st

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Introductie
st.write("Welkom bij de Titanic Data Analyse App! Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren.")

# Navigatie
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Selecteer een sectie:", ["Data Analyse", "Visualisatie", "Algoritme"])

if page == "Data Analyse":
    st.markdown("Ga naar de pagina voor Data Analyse.")
    st.write("Hier kun je gegevens verkennen en basisstatistieken bekijken.")

elif page == "Visualisatie":
    st.markdown("Ga naar de pagina voor Visualisatie.")
    st.write("Hier kun je grafieken en visualisaties bekijken.")

elif page == "Algoritme":
    st.markdown("Ga naar de pagina voor Algoritme.")
    st.write("Hier kun je machine learning modellen toepassen.")

