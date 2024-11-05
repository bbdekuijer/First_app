import streamlit as st

# Hoofdtitel
st.title("Titanic Data Analyse App")

# CSS voor achtergrondafbeelding links onderin
st.markdown(
    """
    <style>
    .background-image {
        position: fixed;
        bottom: 10px;
        left: 10px;
        width: 200px;
        opacity: 0.8;
        z-index: -1;
    }
    </style>
    <img src='Afbeeldingen/HVA.png' class='background-image'>
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

