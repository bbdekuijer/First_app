import streamlit as st

# Hoofdtitel
st.title("Titanic Data Analyse App")

# CSS voor achtergrondafbeelding links onderin
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('Afbeeldingen/HVA.png');
        background-position: left bottom;
        background-repeat: no-repeat;
        background-size: 200px;  /* Pas de grootte van de afbeelding aan zoals gewenst */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Introductie
st.write("Welkom bij de Titanic Data Analyse App! Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren.")
st.write("""
Met behulp van deze app kun je:
- Basisstatistieken van de dataset bekijken.
- Visualisaties genereren over leeftijdsverdeling, passagiersklassen en overlevingskansen.
- Diepgaand analyseren wie er aan boord waren en waar ze vandaan kwamen.

Duik erin en ontdek zelf de patronen en inzichten die de Titanic-data te bieden heeft!
""")
